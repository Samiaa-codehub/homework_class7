import rich
from agents import Agent,Runner,input_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered
from connection import config
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
load_dotenv()

class StudentOutput(BaseModel):
    response:str
    isClassTimingChange:bool


student_with_guardrail=Agent(
    name="Student Guardrail",
    instructions="""you are a student assistant,your task is to ensure that students are not allowed to chnge their class timings. 
    if any student tries to request a change in class timings.
    you must block the request immediately oitherwise you can allow the request.""",
    output_type=StudentOutput
)
@input_guardrail
async def class_timing_guardrail(ctx,agent,input):
    result= await Runner.run(student_with_guardrail,input,run_config=config)
    rich.print(f"Guardrail output: {result.final_output.response}")
    return GuardrailFunctionOutput(
            output_info=result.final_output.response,
            tripwire_triggered=result.final_output.isClassTimingChange,
        )


student_agent=Agent(
    name="student agent",
    instructions="you are a student agent",
    input_guardrails=[class_timing_guardrail]
)
async def main():
    try:
        result=await Runner.run(student_agent,"I want to change my class timings.....",run_config=config)
        print("Request processed")
    except InputGuardrailTripwireTriggered as e:
        rich.print("Guardrail blocked the request...")

if __name__ == "__main__":
    asyncio.run(main())