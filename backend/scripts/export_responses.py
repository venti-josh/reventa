#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
from typing import Any
from uuid import UUID

import httpx
import pandas as pd


# Instead of TypedDict, use a regular dict with type annotation
# This allows for dynamic keys
async def get_responses_from_api(
    survey_instance_id: UUID, api_base_url: str, api_key: str | None = None
) -> list[dict[str, Any]]:
    """Get all responses for a specific survey instance from the API."""
    # The correct endpoint based on the router implementation
    url = f"{api_base_url}/api/v1/survey-instances/{survey_instance_id}/responses"

    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 404:
            print(f"Survey instance {survey_instance_id} not found")
            return []

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return []

        try:
            responses: list[dict[str, Any]] = response.json()
            print(f"Retrieved {len(responses)} responses")
        except json.JSONDecodeError:
            print(f"Error decoding response: {response.text}")
            return []

        # Process the responses
        result: list[dict[str, Any]] = []
        for response_data in responses:
            # Extract answers into separate columns
            processed_response: dict[str, Any] = {
                "id": response_data.get("id"),
                "org_id": response_data.get("org_id"),
                "survey_instance_id": response_data.get("survey_instance_id"),
                "submitted_at": response_data.get("submitted_at"),
                "email_hash": response_data.get("email_hash"),
                "score": response_data.get("score"),
            }

            # Expand answers into individual columns
            answers: dict[str, Any] = response_data.get("answers", {})
            for question, answer in answers.items():
                # Extract the inner value from answer dictionaries
                if isinstance(answer, dict) and "value" in answer:
                    value = answer["value"]
                    # Handle array values (like multiple choice selections)
                    if isinstance(value, list):
                        processed_response[question] = ", ".join(str(v) for v in value)
                    else:
                        processed_response[question] = value
                else:
                    processed_response[question] = answer

            result.append(processed_response)

        return result


async def export_to_csv(
    survey_instance_id: UUID, output_file: str, api_base_url: str, api_key: str | None = None
) -> None:
    """Export survey responses to a CSV file."""
    responses = await get_responses_from_api(survey_instance_id, api_base_url, api_key)

    if not responses:
        print("No responses found")
        return

    # Convert to pandas DataFrame for easy CSV export
    df = pd.DataFrame(responses)

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Exported {len(responses)} responses to {output_file}")


def main() -> None:
    """Parse command line arguments and run export."""
    parser = argparse.ArgumentParser(description="Export survey responses to CSV")
    parser.add_argument("survey_instance_id", help="UUID of the survey instance")
    parser.add_argument("--output", "-o", default="responses.csv", help="Output CSV file path")
    parser.add_argument("--api-url", default="https://reventa.onrender.com", help="Base URL for the Reventa API")
    parser.add_argument("--api-key", help="API key for authentication")

    args = parser.parse_args()

    try:
        survey_instance_id = UUID(args.survey_instance_id)
    except ValueError:
        print("Invalid survey instance ID. Must be a valid UUID.")
        sys.exit(1)

    asyncio.run(export_to_csv(survey_instance_id, args.output, args.api_url, args.api_key))


if __name__ == "__main__":
    main()
