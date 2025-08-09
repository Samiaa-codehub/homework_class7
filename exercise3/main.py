from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
from connection import config
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
load_dotenv()

class GateGuardrailOutput(BaseModel):
    response:str
    isGateKepperChange:bool


Gate_Kepper_guardrail=Agent(
    name="Gate kepper Guardrail",
    instructions="""you are gate kepper guardrail agent . your jobs is to only allow students from our school to enter . if a students belongs to another school, you must stop them from entering  the gate
    """,
    output_type=GateGuardrailOutput
)
@input_guardrail
async def gate_checker_guardrail(ctx,agent,input):
    result= await Runner.run(Gate_Kepper_guardrail,input,run_config=config)
    print(f"Guardrail output: {result.final_output.response}")
    return GuardrailFunctionOutput( 
            output_info=result.final_output.response,
            tripwire_triggered=result.final_output.isGateKepperChange,
        )


gate_kepper_agent=Agent(
    name="Gate kepper agent",
    instructions="you are a Gate kepper agent",
    input_guardrails=[gate_checker_guardrail]
)
async def exercise3_main():
    try:
        result=await Runner.run(gate_kepper_agent," I am a student from our school.....",run_config=config)
        print("Request processed")
    except InputGuardrailTripwireTriggered:
        print("Guardrail blocked the request...")

if __name__ == "__main__":
    asyncio.run(exercise3_main())