# Invoice API

A lightweight REST API for invoice management built with Flask.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

The server starts on `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/invoices` | List all invoices |
| POST | `/invoices` | Create invoice |
| GET | `/invoices/<id>` | Get invoice by ID |
| PUT | `/invoices/<id>` | Update invoice |
| DELETE | `/invoices/<id>` | Delete invoice |
| GET | `/health` | Health check |

## Configuration

Copy `.env.example` to `.env` and set your database credentials:

```bash
cp .env.example .env
```

## Testing

```bash
pip install pytest
pytest tests/ -v
```

## License

MIT
