"""
Webhook Notifier
Sends notifications via webhooks when events occur
"""

import requests
import json
from typing import Dict, Optional, List
from datetime import datetime
import threading

class WebhookNotifier:
    """Sends webhook notifications for video generation events"""
    
    def __init__(self, webhook_urls: Optional[List[str]] = None):
        self.webhook_urls = webhook_urls or []
        self.timeout = 5  # seconds
        self.retry_count = 2
    
    def add_webhook(self, url: str):
        """Add a webhook URL"""
        if url not in self.webhook_urls:
            self.webhook_urls.append(url)
    
    def remove_webhook(self, url: str):
        """Remove a webhook URL"""
        if url in self.webhook_urls:
            self.webhook_urls.remove(url)
    
    def send_notification(
        self,
        event_type: str,
        data: Dict,
        async_send: bool = True
    ) -> bool:
        """
        Send notification to all webhooks
        
        Args:
            event_type: Type of event ('generation_started', 'generation_completed', etc.)
            data: Event data
            async_send: Send asynchronously in background thread
        
        Returns:
            True if sent successfully (for sync), always True for async
        """
        if not self.webhook_urls:
            return True
        
        payload = {
            'event': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        if async_send:
            # Send in background thread
            thread = threading.Thread(
                target=self._send_to_all_webhooks,
                args=(payload,),
                daemon=True
            )
            thread.start()
            return True
        else:
            # Send synchronously
            return self._send_to_all_webhooks(payload)
    
    def _send_to_all_webhooks(self, payload: Dict) -> bool:
        """Send payload to all webhook URLs"""
        all_success = True
        
        for url in self.webhook_urls:
            success = self._send_to_webhook(url, payload)
            if not success:
                all_success = False
        
        return all_success
    
    def _send_to_webhook(self, url: str, payload: Dict) -> bool:
        """Send payload to a single webhook URL with retry"""
        for attempt in range(self.retry_count + 1):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=self.timeout,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code in [200, 201, 202, 204]:
                    return True
                else:
                    print(f"Webhook {url} returned status {response.status_code}")
            
            except requests.Timeout:
                print(f"Webhook {url} timeout (attempt {attempt + 1}/{self.retry_count + 1})")
            except Exception as e:
                print(f"Webhook {url} error: {e}")
            
            if attempt < self.retry_count:
                # Wait before retry
                import time
                time.sleep(1)
        
        return False
    
    def notify_generation_started(self, prompt: str, job_id: str):
        """Notify that video generation has started"""
        self.send_notification('generation_started', {
            'job_id': job_id,
            'prompt': prompt
        })
    
    def notify_generation_completed(
        self,
        prompt: str,
        job_id: str,
        video_path: str,
        duration: float
    ):
        """Notify that video generation completed successfully"""
        self.send_notification('generation_completed', {
            'job_id': job_id,
            'prompt': prompt,
            'video_path': video_path,
            'duration': duration,
            'success': True
        })
    
    def notify_generation_failed(
        self,
        prompt: str,
        job_id: str,
        error: str
    ):
        """Notify that video generation failed"""
        self.send_notification('generation_failed', {
            'job_id': job_id,
            'prompt': prompt,
            'error': error,
            'success': False
        })
    
    def notify_system_event(self, event: str, details: Dict):
        """Notify about system events"""
        self.send_notification('system_event', {
            'event': event,
            'details': details
        })


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("WEBHOOK NOTIFIER - TEST")
    print("=" * 60)
    
    # Create notifier (with mock webhook URL)
    notifier = WebhookNotifier()
    notifier.add_webhook("https://webhook.site/your-unique-url")
    
    # Test notifications
    print("\nSending test notifications...")
    
    notifier.notify_generation_started("ocean waves", "job_123")
    print("✅ Sent: generation_started")
    
    notifier.notify_generation_completed(
        "ocean waves",
        "job_123",
        "/outputs/video_123.mp4",
        29.3
    )
    print("✅ Sent: generation_completed")
    
    notifier.notify_generation_failed(
        "invalid prompt",
        "job_456",
        "Timeout error"
    )
    print("✅ Sent: generation_failed")
    
    print("\n✅ All notifications sent (check webhook.site)")
