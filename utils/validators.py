#Allowed travel types as per requirements

VALID_TRAVEL_TYPES = ["Budget","Luxury","Adventure","Family"]


def validate_deal_data(data):
    """
     validate the input data for a travel deal.
     returns:
     1.whether the data is valid or not
     2.list of error message
    """

    errors = []


    #check required fields exist 
    
    required_fields = ["destination", "travel_type", "price", "duration"]
    for field in required_fields:
        if field not in data:
            errors.append(f"'{field}' field is required.")

    #if required fields missing, no point checking further values
    if errors:
        return False, errors

    #validate destination - it can not be empty
    if not isinstance(data["destination"],str) or data["destination"].strip() == "":
        errors.append("destination can not be empty.")

    #validate price - it must be a positive number
    if not isinstance(data["price"],(int,float)) or data["price"] <= 0:
        errors.append("price must be a positive number.")

    #validate rating include 1 to 5
    if (data["rating"],(int,float)) or not (1 <= data["rating"] <= 5):
        errors.append("rating must be between 1 and 5.")

    #validate travel type it must be inside the allowed list
    if data["travel_type"] not in VALID_TRAVEL_TYPES:
        errors.append(
            f"travel_type musr be one of {VALID_TRAVEL_TYPES}."
        )

    if not isinstance(data["platfrom"],str) or data["platfrom"].strip() == "":
        errors.append("platfrom can not be empty.")

    return (len(errors) == 0), errors