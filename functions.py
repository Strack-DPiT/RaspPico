def parse_data(userData):
    parsed_string = "L"
    if(len(userData["user_id"]) <= 8):
        parsed_string += userData["user_id"]
        number = 8 - len(userData["user_id"])
        parsed_string += "*" * number;
    parsed_string += str(userData["lat"])
    parsed_string += str(userData["long"])
    return parsed_string
    

def reverse_parse_data(lora_data):
    if lora_data[0] != 'L':
        raise ValueError("Invalid lora_data format")

    user_id = lora_data[1:9].replace('*','')
    lat = float(lora_data[9:15])
    long = float(lora_data[15:21])

    data_dict = {
        "user_id": user_id,
        "lat": lat,
        "long": long
    }
    return data_dict