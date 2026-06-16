from flask import Blueprint, jsonify
from services.deal_service import stats_service

# Separate blueprint no / deals prefix, since /stats is a top - level endpoint
stats_bp = Blueprint('stats', __name__, url_prefix='/stats')



@stats_bp.route('',methods=['GET'])
def fet_stats():
    """
    GET /stats
    Returns API usage statistics.
    """

    stats = stats_service.get_stats()

    return jsonify({
        "status": "success",
        "data": stats
    }), 200