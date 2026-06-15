from flask import Blueprint, request, jsonify
from services.deal_service import deal_service
from utils.logger import logger


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

@deal_bp.route('/search', methods=['GET'])
def search_deals():
    """
    GET /deals/search?destination=dubai&platform=booking&travel_type=Luxury
    Partial, case-insensitive search.
    """

    params = request.args

    results, error = deal_service.search_deals(params)

    if error:
        return jsonify({
            "status": "error",
            "message": "Search validtion failed.",
            "details": error["errors"]
        }), 400

    if not results:
        return jsonify({
            "status": "success",
            "message": "No deals found matching your search.",
            "count": 0,
            "data": []
        }), 200

    return jsonify({
        "status": "success",
        "count": len(results),
        "data": results
    }), 200

@deal_bp.route('/filter', methods=['GET'])
def filter_deals():
    """
    GET /deals/filter?min_price=1000&max_price=5000
    Filters deals by price range.
    """

    params = request.args

    results, error = deal_service.filter_deals(params)

    if error:
        return jsonify({
            "status": "error",
            "message": "Filter validation failed.",
            "details": error["errors"]
        }), 400

    if not results:
        return jsonify({
            "status": "success",
            "message": "No deals found in this price range.",
            "count": 0,
            "data": []
        }), 200

    return jsonify({
        "status": "success",
        "count": len(results),
        "data": results
    }), 200

@deal_bp.route('/sort', methods=['GET'])
def sort_deals():
    """
    GET /deals/sort?sort_by=price&order=asc
    Sorts deals by the specified field and order.
    """
    params = request.args

    results, error = deal_service.sort_deals(params)

    if error:
        return jsonify({
            "status": "error",
            "message": "Sort validation failed",
            "details": error["errors"]
        }), 400

    return jsonify({
        "status": "success",
        "count": len(results),
        "data": results
    }), 200

@deal_bp.route('/recent', methods=['GET'])
def get_recently_viewed():
    """
    GET /deals/recent
    Returns recently viewed deals (last 10, most recent first).
    """

    recent = deal_service.get_recently_viewed()

    if not recent:
        return jsonify({
            "status": "success",
            "message": " no recently viewed deals.",
            "count": 0,
            "data": []
        }), 200

    return jsonify({
        "status": "success",
        "count": len(recent),
        "data": recent
    }), 200

@deal_bp.route('/<int:deal_id>',methods=['GET'])
def get_deal(deal_id):
    """
    Returns the deal for a specific ID.
    """

    deal,error = deal_service.get_deal_by_id(deal_id)

    if error:
        return jsonify({
            "status": "error",
            "message": error["errors"][0]
        }),404

    return jsonify({
        "status": "success",
        "data": deal
    }),200
