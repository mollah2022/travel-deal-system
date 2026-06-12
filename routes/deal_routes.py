from flask import Blueprint, request, jsonify
from services.deal_service import deal_service


# Creating a blueprint named deals with the '/deals' URL prefix.
deal_bp = Blueprint('deals',__name__, url_prefix='/deals')

@deal_bp.route('',methods=['POST'])
def create_deal():
    """
    Create a new travel deal.
    """
    data = request.get_json(silent=True)


    # if JSON body is missing.
    if data is None:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON."
        }),400
    
    deal,error = deal_service.create_deal(data)

    if error:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "details": error["error"]
        }),400
    
    return jsonify({
        "status": "success",
        "message": "Travel deal created successfully.",
        "data": deal
    }),201


@deal_bp.route('',methods=['GET'])
def get_all_deals():
    """
    Returns the list of all travel deals.
    """

    deals = deal_service.get_all_deals()

    return jsonify({
        "status":"success",
        "count": len(deals),
        "data": deals
    }),200


@deal_bp.route('/<int:deal_id>',methods=['GET'])
def get_deal(deal_id):
    """
    Returns the deal for a specific ID.
    """

    deal,error = deal_service.get_deal_by_id(deal_id)

    if error:
        return jsonify({
            "status": "error",
            "message": error["error"][0]
        }),404

    return jsonify({
        "status": "success",
        "data": deal
    }),200
