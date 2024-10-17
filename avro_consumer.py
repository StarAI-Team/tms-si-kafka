from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import OperationalError  
import logging
import os
from confluent_kafka import Consumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext
from schema_registry_client import SchemaClient
import utils
import threading
import logging_config
from flask_wtf import CSRFProtect

# Initialize PostgreSQL connection
def create_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host='db',
        port='5432'
    )
    return conn

# @app.before_first_request
def start_consumer():
    utils.load_env()
    logging_config.configure_logging()

    bootstrap_server = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
    topic = os.environ.get("KAFKA_TOPIC")
    group_id = os.environ.get("CONSUMER_GROUP_ID", "consumer-group-id")
    schema_registry_url = os.environ.get("SCHEMA_REGISTRY_URL")
    schema_type = "AVRO"

    with open("./schemas/schema.avsc") as avro_schema_file:
        avro_schema = avro_schema_file.read()
    schema_client = SchemaClient(schema_registry_url, topic, avro_schema, schema_type)
    schema_str = schema_client.get_schema_str()
    
    consumer = Consumer({
        "bootstrap.servers": bootstrap_server,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
    })
    avro_deserializer = AvroDeserializer(schema_client.schema_registry_client, schema_str)
    consumer.subscribe([topic])

    def consume_messages():
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logging.error(f"Consumer error: {msg.error()}")
                    continue
                byte_message = msg.value()
                decoded_message = avro_deserializer(byte_message, SerializationContext(topic, MessageField.VALUE))
                logging.info(f"Decoded message: {decoded_message}, Type: {type(decoded_message)}")

                task_name = decoded_message['event_name'] if isinstance(decoded_message, dict) else decoded_message
                if task_name:
                    # Transporter registration
                    if task_name == "transporterRegistration_Representative Details":
                        logging.info(f"Received data for committing: {task_name}")
                        
                        user_id = decoded_message["user_id"]
                        company_email = decoded_message["company_email"]
                        company_name = decoded_message["company_name"]
                        company_location = decoded_message["company_location"]
                        first_name = decoded_message["first_name"]
                        id_number = decoded_message["id_number"]
                        last_name = decoded_message["last_name"]
                        phone_number = decoded_message["phone_number"]

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO transporter (user_id, company_email, company_name, company_location, first_name, id_number, last_name, phone_number)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (company_email) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, company_email, company_name, company_location, first_name, id_number, last_name, phone_number))
                            conn.commit()
                            logging.info("Data inserted into transporter.")
                            

                            # return response to client (succefful insertion or cokmpany already exists)
                    if task_name == "transporterRegistration_Company Details":
                        user_id  = decoded_message["user_id"]
                        account_name = decoded_message["account_name"]
                        account_number = decoded_message["account_number"]
                        bank_name = decoded_message["bank_name"]
                        company_contact = decoded_message["company_contact"]
                        directorship = decoded_message["directorship"]
                        proof_of_current_address = decoded_message["proof_of_current_address"]

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO transporter_account_information (user_id, account_name, account_number, bank_name, company_contact, directorship, proof_of_current_address)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, account_name,  account_number, bank_name, company_contact, directorship, proof_of_current_address))
                            conn.commit()
                            logging.info("transporterRegistration_Company Details inserted")

                    if task_name == "transporterRegistration_Company Documentation":
                         # Extract relevant fields
                        user_id = decoded_message["user_id"]
                        certificate_of_incorporation = decoded_message.get("certificate_of_incorporation", "")
                        operators_licence = decoded_message.get("operators_licence", "")
                        operators_expiry = decoded_message.get("operators_expiry", "")
                        permit_expiry = decoded_message.get("permit_expiry", "")
                        permits = decoded_message.get("permits", "")
                        tax_clearance = decoded_message.get("tax_clearance", "")
                        tax_expiry = decoded_message.get("tax_expiry", "")
                        tracking_licence = decoded_message.get("tracking_licence", "")

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO transporter_documentation (user_id, certificate_of_incorporation,operators_licence,  operators_expiry, permit_expiry, permits, tax_clearance,tax_expiry, tracking_licence)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, certificate_of_incorporation, operators_licence, operators_expiry, permit_expiry, permits, tax_clearance,tax_expiry, tracking_licence))
                            conn.commit()
                            logging.info("transporterRegistration_Company Documentation inserted")

                    if task_name == "transporterRegistration_Fleet Management":
                        user_id = decoded_message.get("user_id", "")
                        certificate_of_fitness = decoded_message.get("certificate_of_fitness", "")
                        num_of_trucks = decoded_message.get("num_of_trucks", "")
                        number_of_trucks = decoded_message.get("number_of_trucks", "")
                        reg_books = decoded_message.get("reg_books", "")

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO transporter_fleet (user_id, certificate_of_fitness, num_of_trucks, number_of_trucks, reg_books)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, certificate_of_fitness, num_of_trucks, number_of_trucks, reg_books))
                            conn.commit()
                            logging.info("transporterRegistration_Fleet Management inserted")

                    if task_name == "transporterRegistration_Security":
                        user_id = decoded_message.get("user_id", "")
                        profile_picture = decoded_message.get("profile_picture", "")
                        password = decoded_message.get("password", "")
                
                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO transporter_profile (user_id, profile_picture, password)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, profile_picture, password))
                            conn.commit()
                            logging.info("transporterRegistration_Security inserted")

                    # shipper registration
                    if task_name == "shipperRegistration_Representative Details":

                        user_id = decoded_message.get("user_id", "")
                        first_name = decoded_message.get("first_name", "")
                        last_name = decoded_message.get("last_name", "")
                        phone_number = decoded_message.get("phone_number", "")
                        id_number = decoded_message.get("id_number", "")
                        company_name = decoded_message.get("company_name", "")
                        company_location = decoded_message.get("company_location", "")
                        company_email = decoded_message.get("company_email", "")

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO shipper (user_id, first_name, last_name, phone_number, id_number, company_name, company_location, company_email)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, first_name, last_name, phone_number, id_number, company_name, company_location, company_email))
                            conn.commit()
                            logging.info("shipperRegistration_Details inserted")

                    if task_name == "shipperRegistration_Company Details":
                        user_id = decoded_message.get("user_id", "")
                        company_contact = decoded_message.get("company_contact", "")
                        bank_name = decoded_message.get("bank_name", "")
                        account_name = decoded_message.get("account_name", "")
                        account_number = decoded_message.get("account_number", "")
                        directorship = decoded_message.get("company_email", "")
                        proof_of_current_address = decoded_message.get("company_email", "")

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO shipper_company_details (user_id, company_contact, bank_name, account_name, account_number, directorship, proof_of_current_address)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, company_contact, bank_name, account_name, account_number, directorship, proof_of_current_address))
                            conn.commit()
                            logging.info("tshipperCompany Details inserted")

                    if task_name == "shipperRegistration_Company Documentation":   
                        user_id = decoded_message.get("user_id", "")
                        tax_expiry = decoded_message.get("tax_expiry", "")
                        certificate_of_incorporation = decoded_message.get("certificate_of_incorporation", "")
                        tax_clearance = decoded_message.get("tax_clearance", "")

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO shipper_documentation (user_id, tax_expiry, certificate_of_incorporation, tax_clearance)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, tax_expiry, certificate_of_incorporation, tax_clearance))
                            conn.commit()
                            logging.info("shipperCompany Documentation inserted")

                    if task_name == "shipperRegistration_Security":   
                        user_id = decoded_message.get("user_id", "")
                        password = decoded_message.get("password", "")
                        profile_picture = decoded_message.get("profile_picture", "")

                        conn = create_connection()
                        with conn.cursor() as cur:
                            insert_query = """
                                INSERT INTO shipper_profile (user_id, password, profile_picture)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (user_id) DO NOTHING
                            """

                            # Execute the insert with all values
                            cur.execute(insert_query, (user_id, password, profile_picture))
                            conn.commit()
                            logging.info("shipper security details inserted")

            
                else:
                    logging.warning("No valid task name received.")
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.start()
    logging.info("Consumer started automatically on application startup.")

try:
    start_consumer()
except Exception as e:
    logging.info(e)
# @app.route('/')
# def index():
#     conn = create_connection()
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM transporter")
#         tasks = cur.fetchall()
#         return jsonify({"message": "Tasks:", "data": [{"id": t[0], "name": t[1]} for t in tasks]})

# @app.route('/api/v1/client', methods=['GET'])
# @csrf.exempt
# def get_client_data():
#     conn = create_connection()
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM client")
#         tasks = cur.fetchall()
#         return jsonify({"message": "Client Data:", "data": [{"id": t[0], "name": t[1]} for t in tasks]})

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=7000, debug=True)
