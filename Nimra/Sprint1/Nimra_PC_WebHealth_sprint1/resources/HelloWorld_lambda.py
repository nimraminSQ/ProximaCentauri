def lambda_handler(event, context):
    # This function simply takes the First and last name as input and returns Hello f_name l_name
    return f"Hello {event['first_name']} {event['first_name']}"