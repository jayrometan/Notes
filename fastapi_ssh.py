"""
In this example, the run_command function takes a hostname, command, username, and password as arguments, and connects to the specified host using AsyncSSH to run the command. The function returns a tuple containing the hostname and the output of the command.

The execute_commands endpoint takes a list of hostnames, a list of commands to run on each host, and a username and password to use for authentication. It creates a list of tasks to run the run_command function for each hostname and command, and then uses asyncio.gather to run all of the tasks in parallel.

The results are combined into a dictionary, where the keys are the hostnames and the values are lists of command outputs. This dictionary is then returned as the response
"""

import asyncio
import asyncssh
from fastapi import FastAPI

app = FastAPI()

async def run_command(hostname, command, username, password):
    async with asyncssh.connect(hostname, username=username, password=password) as conn:
        result = await conn.run(command)
        return (hostname, result.stdout)

@app.post("/execute_commands")
async def execute_commands(hostnames: list, commands: list, username: str, password: str):
    tasks = []
    for hostname in hostnames:
        for command in commands:
            tasks.append(run_command(hostname, command, username, password))
    results = await asyncio.gather(*tasks)
    output = {}
    for hostname, result in results:
        if hostname not in output:
            output[hostname] = []
        output[hostname].append(result)
    return output

