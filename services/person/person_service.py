import uuid

from services.person.person_database import person_database


class PersonService:

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
        photo,
        embedding
    ):

        full_name = " ".join(
            filter(
                None,
                [
                    first_name,
                    middle_name,
                    last_name
                ]
            )
        )

        person_database.cursor.execute(
            """
            INSERT INTO persons(
                uuid,
                first_name,
                middle_name,
                last_name,
                full_name,
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
                photo,
                embedding
            )
            VALUES(
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?
            )
            """,
            (
                str(uuid.uuid4()),
                first_name,
                middle_name,
                last_name,
                full_name,
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
                photo,
                embedding
            )
        )

        person_database.connection.commit()


person_service = PersonService()