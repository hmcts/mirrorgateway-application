
-- Recipient Endpoint Table
----------------------------
ALTER TABLE recipient_endpoint
ADD CONSTRAINT re_schema_id_fk
FOREIGN KEY (schema_id)
REFERENCES schema_details(schema_id)
NOT DEFERRABLE INITIALLY IMMEDIATE
;

-- Message Map Table
--------------------
ALTER TABLE message_map
ADD CONSTRAINT mm_recipient_endpoint_id_fk
FOREIGN KEY (recipient_endpoint_id)
REFERENCES recipient_endpoint(recipient_endpoint_id)
NOT DEFERRABLE INITIALLY IMMEDIATE
;

ALTER TABLE message_map
ADD CONSTRAINT mm_schema_id_fk
FOREIGN KEY (schema_id)
REFERENCES schema_details(schema_id)
NOT DEFERRABLE INITIALLY IMMEDIATE
;

-- Audit Table 
--------------
ALTER TABLE message_audit
ADD CONSTRAINT ma_message_status_id_fk
FOREIGN KEY (message_status_id)
REFERENCES message_status(message_status_id)
NOT DEFERRABLE INITIALLY IMMEDIATE
;
