import streamlit as st
from confluent_kafka import Producer
import socket

conf = {
    "bootstrap.servers": "abc.us-west4.gcp.confluent.cloud:9092",
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "yourusername",
    "sasl.password": "yourpassword",
    "client.id": socket.gethostname(),
}

producer = Producer(conf)


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


topic = "illegal_dumping"
# Wait up to 1 second for events. Callbacks will be invoked during
# this method call if the message is acknowledged.
producer.poll(1)


def report_incident(incident_type, location, description, contact):
    """
    Function to send incident report data to Kafka
    """
    report_data = f"{{'incident_type': '{incident_type}', 'location': '{location}', 'description': '{description}', 'contact': '{contact}'}}"
    producer.produce(topic, key="key", value=report_data, callback=acked)
    st.success("Incident reported successfully!")


st.title("Environmental Incident Reporting Tool")

incident_type = st.selectbox(
    "Incident Type", ("Illegal Dumping", "Pollution", "Deforestation", "Other")
)
location = st.text_input("Location (Address or Description)")
description = st.text_area("Description (Optional)")
contact = st.text_input("Contact Information (Optional)", key="contact")

if st.button("Report Incident"):
    report_incident(incident_type, location, description, contact)
