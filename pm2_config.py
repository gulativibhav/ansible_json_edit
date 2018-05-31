# !/usr/bin/python

import json
import sys


def add_latest( config, server_details_dict):
  pm2_server_config = server_details_dict
  root_directory = pm2_server_config["root_directory"]
  process_name = 'web-api'
  directory_path = root_directory + '/latest'
  node_port = pm2_server_config["node_port"]
  node_env = pm2_server_config["node_env"]
  template_config = {
          "name": process_name,
          "script": "server.js",
          "merge_logs": True,
          "exec_mode": "cluster",
          "instances": 0,
          "autorestart": True,
          "error_file": "/var/log/pm2/stderr.log",
          "out_file": "/var/log/pm2/stdout.log",
          "cwd": directory_path,
          "env": {
              "PROCESS_NAME": process_name,
              "NODE_PORT": node_port,
              "NODE_ENV": node_env,
              "http_proxy": "http://10.251.38.158:8008",
              "https_proxy": "http://10.251.38.158:8008"
              }
          }
  config_list.append(template_config)

def add( config_list, server_details_dict):
  pm2_server_config = server_details_dict
  root_directory = pm2_server_config["root_directory"]
  branch = pm2_server_config["branch"]
  directory_name = pm2_server_config["directory_name"]
  process_name = branch + '-' + directory_name
  directory_path = root_directory + '/' + branch + '/' + directory_name
  node_port = pm2_server_config["node_port"]
  node_env = pm2_server_config["node_env"]
  template_config = {
          "name": process_name,
          "script": "server.js",
          "merge_logs": True,
          "exec_mode": "cluster",
          "instances": 0,
          "autorestart": True,
          "error_file": "/var/log/pm2/stderr.log",
          "out_file": "/var/log/pm2/stdout.log",
          "cwd": directory_path,
          "env": {
              "PROCESS_NAME": process_name,
              "NODE_PORT": node_port,
              "NODE_ENV": node_env,
              "http_proxy": "http://10.251.38.158:8008",
              "https_proxy": "http://10.251.38.158:8008"
              }
          }
  config_list.append(template_config)

def remove( config_list, process_name):
  for i in xrange(len(config_list)):
    if config_list[i]["name"] == process_name:
      config_list.pop(i)
      break

def check( config_list, process_name):
  for i in xrange(len(config_list)):
    if config_list[i]["name"] == process_name:
      status = "exists"
      break
    else:
      status = "not exists"
  return (status if len(config_list) > 0 else "not exists")


apps_list  = json.load(open("./pm2-web-api.json"))
config_list = apps_list["apps"]

action = sys.argv[1]
if action == "add" and len(sys.argv) == 7:
  server_details_dict = {}
  server_details_dict["root_directory"] = sys.argv[2]
  server_details_dict["branch"] = sys.argv[3]
  server_details_dict["directory_name"] = sys.argv[4]
  server_details_dict["node_port"] = sys.argv[5]
  server_details_dict["node_env"] = sys.argv[6]
  add(config_list, server_details_dict)
elif action == "remove" and len(sys.argv) == 3:
  process_to_delete = sys.argv[2]
  remove(config_list, process_to_delete)
elif action == "check" and len(sys.argv) == 3:
  process_to_check = sys.argv[2]
  status = check(config_list, process_to_check)
  sys.stdout.write(status)
  sys.exit()
elif action == "add_latest" and len(sys.argv) == 5:
  server_details_dict = {}
  server_details_dict["root_directory"] = sys.argv[2]
  server_details_dict["node_port"] = sys.argv[3]
  server_details_dict["node_env"] = sys.argv[4]
  add_latest(config_list, server_details_dict)

else:
  sys.stderr.write("proper usage python <filename> [ add <root_directory> <branch> <directory_name> <node_port> <node_env> | remove <process_to_remove> | check <process_to_check>]")

apps_list["apps"] = config_list


open("./pm2-web-api.json", "w").write(
  json.dumps(apps_list, sort_keys=True, indent=4, separators=(',', ': '))
)