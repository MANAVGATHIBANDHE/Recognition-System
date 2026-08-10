"""
Person Service
Recognition System v2
"""

import numpy as np

from core.logger.logger import app_logger
from services.person.person_database import person_database


class PersonService:

    # ==========================================================
    # CREATE PERSON
    # ==========================================================

    def create_person(

        self,

        first_name,

        middle_name,

        last_name,

        gender,

        dob,

        phone,

        email,

        house,

        area,

        city,

        state,

        country,

        postal_code,

        occupation,

        relationship,

        tags,

        notes,

        photo,

        embedding

    ):

        uid = person_database.create_person(

            first_name=first_name,

            middle_name=middle_name,

            last_name=last_name,

            gender=gender,

            dob=dob,

            phone=phone,

            email=email,

            house=house,

            area=area,

            city=city,

            state=state,

            country=country,

            postal_code=postal_code,

            occupation=occupation,

            relationship=relationship,

            tags=tags,

            notes=notes,

            photo=photo,

            embedding=embedding

        )

        app_logger.success(
            "Person Registered"
        )

        return uid

    # ==========================================================
    # ADD NEW FACE TO EXISTING PERSON
    # ==========================================================

    def add_to_existing(

        self,

        full_name,

        new_embedding

    ):

        data = person_database.get_person_data(
            full_name
        )

        if not data:

            app_logger.warning(
                f"{full_name} not found."
            )

            return False

        old_embedding, recognition_count = data

        person_uuid = person_database.get_person_uuid(
            full_name
        )

        if person_uuid is None:

            return False

        new_embedding = (
            new_embedding.astype("float32")
        )

        new_embedding /= np.linalg.norm(
            new_embedding
        )

        # ------------------------------------------------------
        # First embedding
        # ------------------------------------------------------

        if old_embedding is None:

            person_database.update_person_embedding(

                full_name,

                new_embedding.tobytes(),

                1

            )

            person_database.add_secondary_embedding(

                person_uuid,

                new_embedding.tobytes()

            )

            return True

        # ------------------------------------------------------
        # Existing embedding
        # ------------------------------------------------------

        old_embedding = np.frombuffer(

            old_embedding,

            dtype=np.float32

        ).copy()

        similarity = float(

            np.dot(

                old_embedding,

                new_embedding

            )

        )

        if similarity >= 0.85:

            weight = min(
                recognition_count,
                50
            )

            average = (

                old_embedding * weight +

                new_embedding

            ) / (

                weight + 1

            )

            average /= np.linalg.norm(
                average
            )

            person_database.update_person_embedding(

                full_name,

                average.tobytes(),

                recognition_count + 1

            )

            app_logger.info(

                f"Updated average embedding -> {full_name}"

            )

        elif similarity >= 0.60:

            person_database.add_secondary_embedding(

                person_uuid,

                new_embedding.tobytes()

            )

            person_database.increment_recognition(

                full_name

            )

            app_logger.info(

                f"Added secondary embedding -> {full_name}"

            )

        else:

            app_logger.warning(

                "Embedding too different. Ignored."

            )

            return False

        return True

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_person(

        self,

        full_name

    ):

        person_database.delete_person(
            full_name
        )

        app_logger.info(
            f"Deleted {full_name}"
        )

    # ==========================================================
    # PERSON LIST
    # ==========================================================

    def get_all_persons(self):

        return person_database.get_all_persons()

    def get_all_persons_brief(self):

        return person_database.get_all_persons_brief()


person_service = PersonService()