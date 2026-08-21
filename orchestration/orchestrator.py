from AGENTS import contract_agent,security_agent,implementation_agent,testing_agent,reliability_agent
def run(ctx): return [a.run(ctx) for a in [contract_agent,security_agent,implementation_agent,testing_agent,reliability_agent]]
