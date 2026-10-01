import azure.functions as func
import logging
import json
import uuid
import random
from datetime import datetime
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */2 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def timer_generator(myTimer: func.TimerRequest) -> None:
    # 1. Generate Fake Streaming Data
    songs = ["S101", "S102", "S103", "S104"]
    artists = {"S101": "A01", "S102": "A02", "S103": "A03", "S104": "A01"}
    
    event = {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": datetime.utcnow().isoformat(),
        "song_id": random.choice(songs),
        "device_type": random.choice(["iOS", "Android", "Web", "Desktop"]),
        "country": random.choice(["US", "UK", "CA", "IN", "DE"]),
        "stream_duration_sec": random.randint(30, 300)
    }
    event["artist_id"] = artists[event["song_id"]]
    
    json_data = json.dumps(event)
    file_name = f"stream_{event['event_id']}.json"

    # 2. Connect to ADLS Gen2 (Replace with your details from Notepad!)
    account_name = "adlsstreamanalytics01"
    client_id = " "
    tenant_id = " "
    client_secret = " "
    
    account_url = f"https://{account_name}.dfs.core.windows.net"
    
    try:
        # Authenticate using the Service Principal we created earlier
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
        
        file_system_client = service_client.get_file_system_client(file_system="bronze")
        file_client = file_system_client.get_file_client(file_name)
        
        # Upload the JSON file directly to the Bronze container
        file_client.upload_data(json_data, overwrite=True)
        logging.info(f"Successfully uploaded {file_name} to Bronze layer.")
    except Exception as e:
        logging.error(f"Error uploading to Data Lake: {e}")