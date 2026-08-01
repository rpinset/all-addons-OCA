from unittest.mock import Mock

from odoo.tests.common import TransactionCase

from odoo.addons.shopify_connector.lib.bulk import ShopifyBulkError, ShopifyBulkRunner


class FakeDownloadResponse:
    def raise_for_status(self):
        return None

    def iter_lines(self):
        return iter(
            [
                b'{"id":"gid://shopify/Product/1","title":"One"}',
                b"",
                b'{"id":"gid://shopify/Product/2","title":"Two"}',
            ]
        )


class TestShopifyLibBulk(TransactionCase):
    def test_bulk_runner_submits_polls_and_downloads_jsonl(self):
        client = Mock()
        client.execute.side_effect = [
            {
                "bulkOperationRunQuery": {
                    "bulkOperation": {"id": "gid://shopify/BulkOperation/1"}
                }
            },
            {
                "bulkOperation": {
                    "id": "gid://shopify/BulkOperation/1",
                    "status": "RUNNING",
                }
            },
            {
                "bulkOperation": {
                    "id": "gid://shopify/BulkOperation/1",
                    "status": "COMPLETED",
                    "url": "https://storage.example/result.jsonl",
                }
            },
        ]
        download_session = Mock()
        download_session.get.return_value = FakeDownloadResponse()
        sleeps = []
        runner = ShopifyBulkRunner(
            client,
            poll_interval=0.25,
            sleep=sleeps.append,
            download_session=download_session,
        )
        records = runner.run("query { products { edges { node { id } } } }")
        assert [record["title"] for record in records] == ["One", "Two"]
        assert sleeps == [0.25]
        assert client.execute.call_count == 3
        assert client.execute.call_args_list[1].args[1] == {
            "id": "gid://shopify/BulkOperation/1"
        }
        download_session.get.assert_called_once_with(
            "https://storage.example/result.jsonl", timeout=60.0, stream=True
        )

    def test_bulk_runner_raises_for_terminal_failure(self):
        client = Mock()
        client.execute.side_effect = [
            {
                "bulkOperationRunQuery": {
                    "bulkOperation": {"id": "gid://shopify/BulkOperation/1"}
                }
            },
            {
                "bulkOperation": {
                    "id": "gid://shopify/BulkOperation/1",
                    "status": "FAILED",
                    "errorCode": "INTERNAL_SERVER_ERROR",
                }
            },
        ]
        runner = ShopifyBulkRunner(client, sleep=lambda _seconds: None)
        with self.assertRaisesRegex(ShopifyBulkError, "FAILED"):
            runner.run("query { products { edges { node { id } } } }")

    def test_bulk_runner_returns_empty_records_when_shop_has_no_results(self):
        client = Mock()
        client.execute.side_effect = [
            {
                "bulkOperationRunQuery": {
                    "bulkOperation": {"id": "gid://shopify/BulkOperation/1"}
                }
            },
            {
                "bulkOperation": {
                    "id": "gid://shopify/BulkOperation/1",
                    "status": "COMPLETED",
                    "url": None,
                }
            },
        ]
        download_session = Mock()
        runner = ShopifyBulkRunner(
            client, sleep=lambda _seconds: None, download_session=download_session
        )
        assert runner.run("query { products { edges { node { id } } } }") == []
        download_session.get.assert_not_called()
