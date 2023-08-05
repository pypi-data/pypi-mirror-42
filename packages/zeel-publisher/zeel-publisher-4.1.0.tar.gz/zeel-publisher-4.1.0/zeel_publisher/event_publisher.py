"""Event Publisher class, custom exceptions, and helper methods"""
import json
import time
import boto3


class EventPublisherError(Exception):
    """Base class for Event Publisher Exceptions."""
    pass


class CarrierError(EventPublisherError):
    """Exception raised if Carrier is invalid."""

    def __init__(self, message):
        self.message = message


class EventPublisher():
    """
    Class responsible for publishing event messages to a single topic.
    """

    def __init__(self, topic_arn, sns_client_params=None):
        """
        Initializes a Publisher object.

        Parameters
        ----------
        topic_arn : string
            Amazon resource identifier for a particular sns topic.
        sns_client_params : dict
            Dictionary containing parameters necessary for initializing a SNS
            client.
        """

        self.topic_arn = topic_arn
        if sns_client_params:
            self.sns_client = boto3.client('sns', **sns_client_params)
        else:
            self.sns_client = boto3.client('sns')

    def publish(
        self,
        carrier,
        uri,
        operation,
        before,
        after,
        service,
        event_type,
        description,
        triggering_account,
        triggering_identity
    ):
        """
        Publish an event message to the instance's SNS Topic.

        Parameters
        ----------
        carrier : dict
            An OpenTrace TEXT_MAP format carrier.
        uri : string
            The uri at which the event pertains to.
        operation : string
            The HTTP method which triggered the event.
        before : mixed
            The resource the event pertains to before it was modified. This can
            be None to represent Creation for example.
        after : mixed
            The resource the event pertains to after it was modified. This can
            be None to represent Deletion for example.
        service : string
            The name of the service which published the event. Eg. zapi-orders,
            zapi-invoices etc.
        event_type : string
            An enum representing the type of change that occurred. Typically
            used in decision making for sqs handlers.
        description : string
            A human readable description of the event. Not standardized.
        triggering_account : dict
            The account that triggered this change.
        triggering_identity : dict
            The identity that triggered this change.

        Returns
        -------
        mixed
            A Dictionary containing an SNS MessageId if the message was
            published successfully, false otherwise.

        """

        body = {
            'default': {
                'carrier': carrier,
                'uri': uri,
                'operation': operation,
                'before': before,
                'after': after,
                'service': service,
                'event_type': event_type,
                'description': description,
                'triggering_account': triggering_account,
                'triggering_identity': triggering_identity,
                'timestamp': time.time()
            }
        }
        payload = {'Message': json.dumps(body)}
        response = self.sns_client.publish(TopicArn=self.topic_arn, **payload)

        return response
