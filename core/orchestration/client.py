import os
from temporalio.client import Client

class TemporalClient:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TemporalClient, cls).__new__(cls)
        return cls._instance

    async def get_client(self) -> Client:
        """
        Returns a connected Temporal Client.
        Ensure you await this method.
        """
        if self._client is None:
            print("Connecting to Temporal server...")
            try:
                # Local development defaults
                target_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
                self._client = await Client.connect(target_host)
                print(f"Connected to Temporal at {target_host}")
            except Exception as e:
                print(f"Failed to connect to Temporal: {e}")
                raise e
        return self._client

    @classmethod
    async def connect(cls) -> Client:
        """Convenience static method to get a client connection."""
        instance = cls()
        return await instance.get_client()
