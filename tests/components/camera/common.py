"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from unittest.mock import Mock

from homeassistant.components.camera import Camera
from homeassistant.components.camera.webrtc import (
    CameraWebRTCProvider,
    async_register_webrtc_provider,
)
from homeassistant.core import HomeAssistant

EMPTY_8_6_JPEG = b"empty_8_6"
WEBRTC_ANSWER = "a=sendonly"
STREAM_SOURCE = "rtsp://127.0.0.1/stream"


def mock_turbo_jpeg(
    first_width=None, second_width=None, first_height=None, second_height=None
):
    """Mock a TurboJPEG instance."""
    mocked_turbo_jpeg = Mock()
    mocked_turbo_jpeg.decode_header.side_effect = [
        (first_width, first_height, 0, 0),
        (second_width, second_height, 0, 0),
    ]
    mocked_turbo_jpeg.scale_with_quality.return_value = EMPTY_8_6_JPEG
    mocked_turbo_jpeg.encode.return_value = EMPTY_8_6_JPEG
    return mocked_turbo_jpeg


async def add_webrtc_provider(hass: HomeAssistant) -> CameraWebRTCProvider:
    """Add test WebRTC provider."""

    class SomeTestProvider(CameraWebRTCProvider):
        """Test provider."""

        async def async_is_supported(self, stream_source: str) -> bool:
            """Determine if the provider supports the stream source."""
            return True

        async def async_handle_web_rtc_offer(
            self, camera: Camera, offer_sdp: str
        ) -> str | None:
            """Handle the WebRTC offer and return an answer."""
            return "answer"

    provider = SomeTestProvider()
    async_register_webrtc_provider(hass, provider)
    await hass.async_block_till_done()
    return provider
