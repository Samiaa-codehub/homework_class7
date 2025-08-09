from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
from conection import config
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
load_dotenv()

class FatherOutput(BaseModel):
    response:str
    father_warning:bool


father_guardrail=Agent(
    name="Father Guardrail",
    instructions="""you are a father agent.your responsibility is to make sure  your child dose not lower the AC temperature below 26C .
    if the child tries to set the AC  temperature less than 26C , you must block the request immediately.
    if the AC temperature is set to 26C or higher, you can allow the request.
    """,
    output_type=FatherOutput
)
@input_guardrail
async def check_temperature_guardrail(ctx,agent,input):
    result= await Runner.run(father_guardrail,input,run_config=config)
    print(f"Guardrail output: {result.final_output.response}")
    return GuardrailFunctionOutput(
            output_info=result.final_output.response,
            tripwire_triggered=result.final_output.father_warning,
        )


father_agent=Agent(
    name="father agent",
    instructions="you are a father agent",
    input_guardrails=[check_temperature_guardrail]
)
async def exercise2_main():
    try:
        result=await Runner.run(father_agent," I want the A temperature is more than 26C.....",run_config=config)
        print("Request processed")
    except InputGuardrailTripwireTriggered:
        print("Guardrail blocked the request...")

if __name__ == "__main__":
    asyncio.run(exercise2_main())