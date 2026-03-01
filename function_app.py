import azure.functions as func
import logging

app = func.FunctionApp()

@app.timer_trigger(schedule="*/30 * * * * *", arg_name="myTimer")
def hourly_intel_bot(myTimer: func.TimerRequest):
    logging.info("Timer is running.")
