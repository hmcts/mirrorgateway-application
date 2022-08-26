
-- Audit Table 
--------------

--------------------------------------------------------
--  Index to support query to return the rows that matches 
--  message_uuid, from_endpoint, to_endpoint cols.
--  Used for duplcate request check.
--------------------------------------------------------
CREATE INDEX AUDIT_DUPLICATE_CHECK_INDX
ON
MESSAGE_AUDIT ( message_uuid, from_endpoint, to_endpoint);

--------------------------------------------------------
--  Index for MESSAGE_AUDIT_UPDATEDATE
--------------------------------------------------------
CREATE INDEX MA_UPDATEDATE_IDX 
ON MESSAGE_AUDIT (UPDATED_DATE);
  
--------------------------------------------------------
--  Index for MESSAGE_STATUS_ID as it is a foreign key
--------------------------------------------------------
CREATE INDEX MA_MSG_STAT_ID_IDX 
ON MESSAGE_AUDIT (MESSAGE_STATUS_ID);


-- Message Map Table
--------------------

--------------------------------------------------------
--  Index for RECIPIENT_ENDPOINT_ID as it is a foreign key
--  There is a many to one hibernate relationship with the
--  Recipient Endpoint Table which uses this index.
--  Used to validate message header.
--------------------------------------------------------
CREATE INDEX MM_REC_ENDPT_ID_IDX 
ON MESSAGE_MAP (RECIPIENT_ENDPOINT_ID);

--------------------------------------------------------
--  Index for SCHEMA_ID as it is a foreign key
--------------------------------------------------------
CREATE INDEX MM_SCHEMA_ID_IDX 
ON MESSAGE_MAP (SCHEMA_ID);
  

-- Message Status Table
-----------------------

--------------------------------------------------------
--  Index for MESSAGE_STATUS
--------------------------------------------------------
CREATE INDEX MS_MSG_STAT_IDX 
ON MESSAGE_STATUS (MESSAGE_STATUS);


-- Recipient Endpoint Table
----------------------------

--------------------------------------------------------
--  Index for SCHEMA_ID which is a foreign key
--------------------------------------------------------
CREATE INDEX RE_SCH_ID_IDX 
ON RECIPIENT_ENDPOINT (SCHEMA_ID);

--------------------------------------------------------
--  Index to support query to return the row that matches 
--  from_endpoint, to_endpoint, endpoint_status cols.
--  Used to validate message header.
--------------------------------------------------------
CREATE INDEX RE_FROM_TO_STATUS_INDX
ON
RECIPIENT_ENDPOINT ( from_endpoint, to_endpoint, endpoint_status);

--------------------------------------------------------
--  Index to support query to return the row that matches 
--  from_endpoint, to_endpoint cols.
--  Used to validate message header.
--------------------------------------------------------
CREATE INDEX RE_FROM_TO_INDX
ON
RECIPIENT_ENDPOINT ( from_endpoint, to_endpoint );

--------------------------------------------------------
--  Index to support query to return the row that matches 
--  from_url, to_url cols.
--  Used to validate message header.
--------------------------------------------------------
CREATE INDEX RE_FROMURL_TOURL_INDX
ON
RECIPIENT_ENDPOINT ( from_url, to_url );


-- Request Operation Table
----------------------------

--------------------------------------------------------
--  Index to support query to return the row that matches 
--  request_type cols.
--  Used to validate message header.
--------------------------------------------------------
CREATE INDEX RO_REQUEST_TYPE_INDX
ON
REQUEST_OPERATION ( request_type );


-- Acknowledgement Table
-------------------------

--------------------------------------------------------
--  Index to support query to return the row that matches 
--  request_type cols.
--  Used to identify the specfic error details to report.
--------------------------------------------------------
CREATE INDEX ACK_ACKNOWLEDGEMENT_TYPE_INDX
ON
ACKNOWLEDGEMENT ( ACKNOWLEDGEMENT_TYPE );
