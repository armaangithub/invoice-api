"""Invoice API - A lightweight REST API for invoice management."""

from flask import Flask, jsonify, request
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory store (replace with database in production)
invoices = {}


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})


@app.route("/invoices", methods=["GET"])
def list_invoices():
    """List all invoices."""
    return jsonify({"invoices": list(invoices.values()), "total": len(invoices)})


@app.route("/invoices", methods=["POST"])
def create_invoice():
    """Create a new invoice."""
    data = request.get_json()
    if not data or "amount" not in data:
        return jsonify({"error": "amount is required"}), 400

    invoice_id = str(uuid.uuid4())[:8]
    invoice = {
        "id": invoice_id,
        "amount": data["amount"],
        "description": data.get("description", ""),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }
    invoices[invoice_id] = invoice
    return jsonify(invoice), 201


@app.route("/invoices/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    """Get an invoice by ID."""
    invoice = invoices.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify(invoice)


@app.route("/invoices/<invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    """Update an invoice."""
    invoice = invoices.get(invoice_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404

    data = request.get_json()
    if data.get("amount"):
        invoice["amount"] = data["amount"]
    if data.get("description"):
        invoice["description"] = data["description"]
    if data.get("status"):
        invoice["status"] = data["status"]

    return jsonify(invoice)


@app.route("/invoices/<invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    """Delete an invoice."""
    if invoice_id not in invoices:
        return jsonify({"error": "Invoice not found"}), 404

    del invoices[invoice_id]
    return "", 204


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
