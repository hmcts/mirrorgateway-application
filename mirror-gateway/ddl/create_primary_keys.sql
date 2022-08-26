
--
-- recipient endpoint table    
--
CREATE UNIQUE INDEX recipient_endpoint_pk
ON recipient_endpoint 
( recipient_endpoint_id )
;

ALTER TABLE recipient_endpoint
ADD CONSTRAINT recipient_endpoint_pk
PRIMARY KEY
USING INDEX recipient_endpoint_pk
;

--
-- message map table   
--
CREATE UNIQUE INDEX message_map_pk
ON message_map 
( message_map_id )
;

ALTER TABLE message_map
ADD CONSTRAINT message_map_pk
PRIMARY KEY
USING INDEX message_map_pk
;

--
-- message audit table
--
CREATE UNIQUE INDEX message_audit_pk
ON message_audit 
( message_audit_id )
;

ALTER TABLE message_audit
ADD CONSTRAINT message_audit_pk
PRIMARY KEY
USING INDEX message_audit_pk
;

--
-- message status table
--
CREATE UNIQUE INDEX message_status_pk
ON message_status 
( message_status_id )
;

ALTER TABLE message_status
ADD CONSTRAINT message_status_pk
PRIMARY KEY
USING INDEX message_status_pk
;

--
-- schema details table
--
CREATE UNIQUE INDEX schema_details_pk
ON schema_details 
( schema_id )
;

ALTER TABLE schema_details
ADD CONSTRAINT schema_details_pk
PRIMARY KEY
USING INDEX schema_details_pk
;

--
-- request operation table 
--
CREATE UNIQUE INDEX request_operation_pk
ON request_operation 
( request_operation_id )
;

ALTER TABLE request_operation
ADD CONSTRAINT request_operation_pk
PRIMARY KEY
USING INDEX request_operation_pk
;


--
-- acknowledgement table
--
CREATE UNIQUE INDEX acknowledgement_pk
ON acknowledgement 
( acknowledgement_id )
;

ALTER TABLE acknowledgement
ADD CONSTRAINT acknowledgement_pk
PRIMARY KEY
USING INDEX acknowledgement_pk
;
