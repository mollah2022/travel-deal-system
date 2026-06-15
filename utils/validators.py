#Allowed travel types as per requirements
VALID_TRAVEL_TYPES = ["Budget","Luxury","Adventure","Family"]

# Allowed sorting fields
VALID_SORT_FIELDS = ["price","rating","destination"]

# Allowed sorting orders
VALID_SORT_ORDERS = ["asc","desc"]


def validate_deal_data(data):
    """
     validate the input data for a travel deal.
     returns:
     1.whether the data is valid or not
     2.list of error message
    """

    errors = []


    #check required fields exist 
    
    required_fields = ["destination", "price", "platform", "rating", "travel_type"]
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
    if not isinstance (data["rating"],(int,float)) or not (1 <= data["rating"] <= 5):
        errors.append("rating must be between 1 and 5.")

    #validate travel type it must be inside the allowed list
    if data["travel_type"] not in VALID_TRAVEL_TYPES:
        errors.append(
            f"travel_type musr be one of {VALID_TRAVEL_TYPES}."
        )

    if not isinstance(data["platform"],str) or data["platform"].strip() == "":
        errors.append("platfrom can not be empty.")

    return (len(errors) == 0), errors


def validate_search_params(params):
    """
    validate search query parameters.
    At least one of destination, platfrom, travel_type must be provided.
    returns: (is_valid: bool, errors: list)
    """

    errors = []

    destination = params.get("destination", "").strip()
    platform = params.get("platform", "").strip()
    travel_type = params.get("travel_type", "").strip()


    # At least one search param must be provided
    if not destination and not platform and not travel_type:
        errors.append("At least one search parameter is required : destination, platform, or travel_type.")
        return False, errors

    #travel_type provided but invalid value
    if travel_type and travel_type not in VALID_TRAVEL_TYPES:
        errors.append(f"travel_type must be one of {VALID_TRAVEL_TYPES}.")

    return(len(errors) == 0), errors


def validate_filter_params(params):
    """
    validate filter query parameters (min_price, max_price).
    Returns: (is_valid: bool , errors: list)
    """

    errors = []

    min_price = params.get("min_price")
    max_price = params.get("max_price")

    # At least one must be provided
    if min_price is None and max_price is None:
        errors.append("At least one of min_price or max_price is required.")
        return False, errors

    # convert to float and validate
    try:
        if min_price is not None:
            min_price = float(min_price)
            if min_price < 0:
                errors.append("min_price can not be negative.")

        if max_price is not None:
            max_price = float(max_price)
            if max_price < 0:
                errors.append("max_price can not be negative")

        #max must be greater than min
        if min_price is not None and max_price is not None:
            if max_price < min_price:
                errors.append("max_price can not be smaller than min_price.")

    except ValueError:
        errors.append("min_price and max_price must be valid numbers.")

    return (len(errors) == 0), errors


def validate_sort_params(params):
    """
    validate sort query parameters (sort_by, order).
    Returns: (is_valid: bool, errors: list)
    """

    errors = []

    sort_by = params.get("sort_by", "").strip()
    order = params.get("order", "asc").strip().lower()


    # sort_by is required
    if not sort_by:
        errors.append("sort_by parameter is required.")
        return False, errors

    # sort_by must be valid field
    if sort_by not in VALID_SORT_FIELDS:
        errors.append(f"sort_by must be one of {VALID_SORT_FIELDS}.")

    # order must be asc or desc
    if order not in VALID_SORT_ORDERS:
        errors.append(f"order must be one of {VALID_SORT_ORDERS}.")
        
    return (len(errors) == 0), errors