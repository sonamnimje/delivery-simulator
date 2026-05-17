"""
Validation Service for extracted data.
Ensures extracted fields meet business requirements.
"""

from datetime import datetime
from typing import Any, Dict

from loguru import logger

from app.core.exceptions import ValidationException


class ValidationService:
    """
    Validates extracted data against business rules.
    """

    # Validation rules for each document type
    VALIDATION_RULES = {
        "aadhaar": {
            "aadhaar_number": {
                "type": "string",
                "pattern": r"^\d{4}\s\d{4}\s\d{4}$|^\d{12}$",
                "description": "12-digit Aadhaar number",
            },
            "date_of_birth": {
                "type": "date",
                "description": "Valid date",
            },
        },
        "driving_license": {
            "license_number": {
                "type": "string",
                "min_length": 3,
                "description": "License number",
            },
            "expiry_date": {
                "type": "date",
                "description": "Valid date",
            },
        },
        "passport": {
            "passport_number": {
                "type": "string",
                "min_length": 5,
                "description": "Passport number",
            },
            "expiry_date": {
                "type": "date",
                "description": "Valid date",
            },
        },
        "invoice": {
            "invoice_number": {
                "type": "string",
                "min_length": 1,
                "description": "Invoice number",
            },
            "total_amount": {
                "type": "float",
                "description": "Total amount",
            },
        },
    }

    @staticmethod
    def validate_extracted_data(
        extracted_data: Dict[str, Any], document_type: str
    ) -> Dict[str, Any]:
        """
        Validate extracted data against business rules.

        Args:
            extracted_data: Dictionary of extracted fields
            document_type: Type of document

        Returns:
            Dict[str, Any]: Validated data

        Raises:
            ValidationException: If validation fails
        """
        logger.info(f"Starting validation for {document_type} document")

        try:
            # Filter out None values
            cleaned_data = {
                k: v for k, v in extracted_data.items() if v is not None
            }

            rules = ValidationService.VALIDATION_RULES.get(document_type, {})

            for field, value in cleaned_data.items():
                if field in rules:
                    ValidationService._validate_field(
                        field, value, rules[field]
                    )

            logger.info(f"Validation successful for {document_type}")
            return cleaned_data

        except ValidationException:
            raise
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            raise ValidationException(f"Data validation failed: {str(e)}")

    @staticmethod
    def _validate_field(field_name: str, value: Any, rule: Dict[str, Any]):
        """
        Validate individual field against its rule.

        Args:
            field_name: Name of field
            value: Field value
            rule: Validation rule

        Raises:
            ValidationException: If validation fails
        """
        if value is None:
            return

        field_type = rule.get("type")

        # Type validation
        if field_type == "string":
            if not isinstance(value, str):
                raise ValidationException(
                    f"{field_name} must be a string, got {type(value).__name__}"
                )

            # Pattern validation
            if "pattern" in rule:
                import re

                if not re.match(rule["pattern"], value):
                    raise ValidationException(
                        f"{field_name} format is invalid. {rule.get('description', '')}"
                    )

            # Length validation
            if "min_length" in rule:
                if len(value) < rule["min_length"]:
                    raise ValidationException(
                        f"{field_name} must be at least {rule['min_length']} characters"
                    )

        elif field_type == "date":
            ValidationService._validate_date(field_name, value)

        elif field_type == "float":
            try:
                float_value = float(value)
                if float_value < 0:
                    raise ValidationException(
                        f"{field_name} must be a positive number"
                    )
            except (ValueError, TypeError):
                raise ValidationException(
                    f"{field_name} must be a valid number"
                )

    @staticmethod
    def _validate_date(field_name: str, date_value: str):
        """
        Validate date field.

        Args:
            field_name: Name of date field
            date_value: Date value as string

        Raises:
            ValidationException: If date is invalid
        """
        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%B %d, %Y",
            "%d %B %Y",
        ]

        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(str(date_value), fmt)
                logger.debug(f"Date {field_name} validated: {parsed_date}")
                return
            except ValueError:
                continue

        raise ValidationException(
            f"{field_name} has invalid date format. Expected YYYY-MM-DD format."
        )
