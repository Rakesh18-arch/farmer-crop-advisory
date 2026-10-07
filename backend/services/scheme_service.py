from database.db import db
from models.advisory import GovernmentScheme

class SchemeService:
    @staticmethod
    def get_schemes(state: str = None, category: str = None, 
                    crop: str = None, scheme_type: str = None) -> list:
        """
        Retrieves government welfare schemes with multi-criteria filtering.
        """
        query = GovernmentScheme.query

        if scheme_type:
            query = query.filter(GovernmentScheme.scheme_type.ilike(f"%{scheme_type}%"))

        if state:
            # Match state-specific or nationwide ('All India') schemes
            query = query.filter(
                (GovernmentScheme.applicable_state.ilike(f"%{state}%")) | 
                (GovernmentScheme.applicable_state.ilike("%All India%"))
            )

        if category:
            query = query.filter(
                (GovernmentScheme.farmer_category.ilike(f"%{category}%")) |
                (GovernmentScheme.farmer_category.ilike("%All Farmers%"))
            )

        if crop:
            query = query.filter(
                (GovernmentScheme.applicable_crops.ilike(f"%{crop}%")) |
                (GovernmentScheme.applicable_crops.ilike("%All Crops%"))
            )

        schemes = query.order_by(GovernmentScheme.scheme_type.asc(), GovernmentScheme.scheme_name.asc()).all()
        return [s.to_dict() for s in schemes]

    @staticmethod
    def get_scheme_by_id(scheme_id: int):
        scheme = GovernmentScheme.query.get(scheme_id)
        return scheme.to_dict() if scheme else None

    @staticmethod
    def create_or_update_scheme(data: dict, scheme_id: int = None) -> tuple:
        """Allows administration to add or update welfare programs."""
        if scheme_id:
            scheme = GovernmentScheme.query.get(scheme_id)
            if not scheme:
                return None, "Scheme not found."
        else:
            scheme = GovernmentScheme()
            db.session.add(scheme)

        scheme.scheme_name = data.get("scheme_name", scheme.scheme_name)
        scheme.description = data.get("description", scheme.description)
        scheme.eligibility = data.get("eligibility", scheme.eligibility)
        scheme.benefits = data.get("benefits", scheme.benefits)
        scheme.required_documents = data.get("required_documents", scheme.required_documents)
        scheme.application_link = data.get("application_link", scheme.application_link)
        scheme.scheme_type = data.get("scheme_type", scheme.scheme_type)
        scheme.applicable_state = data.get("applicable_state", scheme.applicable_state)
        scheme.applicable_crops = data.get("applicable_crops", scheme.applicable_crops)
        scheme.farmer_category = data.get("farmer_category", scheme.farmer_category)

        db.session.commit()
        return scheme.to_dict(), ""
