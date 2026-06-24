from django.test import Client, SimpleTestCase


class HealthApiTests(SimpleTestCase):
    def test_health_endpoint_returns_ok(self):
        response = Client().get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_allows_frontend_loopback_origin(self):
        response = Client().get(
            "/api/health",
            HTTP_ORIGIN="http://127.0.0.1:5173",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Access-Control-Allow-Origin"],
            "http://127.0.0.1:5173",
        )

    def test_api_docs_render(self):
        response = Client().get("/api/docs")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"swagger-ui", response.content.lower())
