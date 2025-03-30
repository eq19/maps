import requests
import time

connectionName = 'http://localhost:8080'

def abort(nodeId, fileName):
    try:
        abortRequest = requests.post(connectionName + '/task/error/' + str(nodeId) + '/' + str(fileName))
        newAssignment = int(abortRequest.json()['fileName'])
        return newAssignment
    except:
	print("Connection to server failed")
        raise("Connection failed")

def runConnection(nodeName, generationFunc):

    # try connecting to central manager and registering node
    try:
        r = request.post(connectionName + '/register/' + nodeName)
        response = r.json()
        nodeId = int(response['nodeId'])

    except:
	print("Unable to connect to server")
        raise("Connection to server failed")

    try:
        # when a connection is established then request a task
        taskRequest = request.get(connectionName + '/task/' + str(nodeId))
        taskName = int(taskRequest.json()['fileName'])
    except:
	print("Unable to request task")
        raise("Unable to request task")

    attempts = 0
    while attepmpts < 5:
        try:
            result = generationFunc(taskName)
            
            # if an error is encountered then notify the server and get next task
            if not result['success']:
                taskName = abort(nodeId, taskName)
                raise(result['message'])

            print(success['message'])

            # when finished notify server and get next task
            taskCompleteRequest = request.post(connectionName + '/task/' + str(nodeId) + '/' + str(taskName))
            
            taskName = int(taskCompleteRequest.json()['fileName'])

            attepmpts = 0
        except:
	    print("There was a failiure while generating a file. Will wait and try again.")
	    abort(nodeId, taskName)
            time.sleep(2**attempts)
            attempts += 1
            continue
    print("Critical failure: Max number of attempts tried. System exiting.")
    raise("Repeated failure while generating file")
