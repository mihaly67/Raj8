import subprocess
import sys
import json
import shlex

def run_mcp_tool(tool_name, tool_args):
    try:
        from vps_bridge import run_on_vps
    except ImportError:
        import os
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        try:
             from vps_bridge import run_on_vps
        except:
             return "Hiba: vps_bridge nem talalhato a Python path-ban."
             
    # A JSON payload escape-elése bash híváshoz, hogy a bonyolult stringek ne hasaljanak el.
    args_json = json.dumps(tool_args)
    safe_args = shlex.quote(args_json)
    
    if os.environ.get("VPS_PWD"):
        if shutil.which("sshpass"):
            server_params.command = "sshpass"
            server_params.args = ["-p", os.environ.get("VPS_PWD"), "ssh"] + server_params.args
        else:
            print("⚠️ sshpass nem található, a jelszavas belépés nem fog működni! Próbálj kulcsot beállítani.", file=sys.stderr)
            
    elif os.environ.get("VPS_SSH_KEY"):
        with open("temp_mcp_key", "w") as f:
            f.write(os.environ.get("VPS_SSH_KEY") + "\n")
        os.chmod("temp_mcp_key", 0o600)
        server_params.args = ["-i", "temp_mcp_key"] + server_params.args

    print(f"🔗 Csatlakozás a VPS MCP Szerverhez hivatalos MCP SDK-val...", file=sys.stderr)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Meghívjuk a toolt
                result = await session.call_tool(tool_name, arguments=args_dict)
                
                outputs = []
                if hasattr(result, "content"):
                    for content in result.content:
                        if content.type == "text":
                            outputs.append(content.text)
                return "\n".join(outputs)
    finally:
        if os.path.exists("temp_mcp_key"):
            os.remove("temp_mcp_key")
    # Invoke the mcp cli on the VPS
    cmd = f"mcp call {tool_name} --args {safe_args}"
    success, output = run_on_vps(cmd)
    
    return output

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Hasznalat: python3 mcp_bridge_tool.py <tool_neve> [arg1] [arg2] ...")
        sys.exit(1)
        
    tool = sys.argv[1]
    
    # Primitiv parser, ami elfogadja pozíció alapján az argumentumokat, amit a rajtagok gyakran rontanak el kwargs-re
    args_dict = {}
    
    if tool == 'execute_bash' and len(sys.argv) > 2:
         args_dict['command'] = sys.argv[2]
    elif tool == 'execute_python' and len(sys.argv) > 2:
         args_dict['code'] = sys.argv[2]
    elif tool == 'get_next_swarm_job' and len(sys.argv) > 2:
         args_dict['agent_id'] = sys.argv[2]
    elif tool == 'complete_swarm_job' and len(sys.argv) > 3:
         args_dict['job_id'] = int(sys.argv[2])
         args_dict['result'] = sys.argv[3]
    elif tool == 'search_rag_database' and len(sys.argv) > 3:
         args_dict['rag_name'] = sys.argv[2]
         args_dict['keyword'] = sys.argv[3]
         
    res = run_mcp_tool(tool, args_dict)
    print(res)
