
--
-- Message Status table data 
--
INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'RECEIVED');

INSERT INTO message_status(message_status_id ,message_status) VALUES ( DEFAULT,'SCHEMA ERROR');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'PROCESSING');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'QUEUED');

INSERT INTO message_status(message_status_id ,message_status) VALUES ( DEFAULT,'DEQUEUED');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'HTTP SENT');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'HTTP RECEIVED');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'PROCESSED OK');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'PROCESSED FAILED');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'COMPLETED');

INSERT INTO message_status(message_status_id,message_status) VALUES ( DEFAULT,'ERRORED');


--
-- Schema Details table data 
--
INSERT INTO schema_details(schema_id,schema_version) VALUES ( DEFAULT,'V0_1');

--
-- Acknowledgement table data
--
INSERT INTO acknowledgement(acknowledgement_id, acknowledgement_type, generic_code, generic_text)
values(DEFAULT, 'REQUEST_PROCESSING_ERROR', 'MGW-999901', 'Request could not be satisfied at this time. Please re-try, if the problem persists then please contact the ATOS Help Desk.'); 

INSERT INTO acknowledgement(acknowledgement_id, acknowledgement_type, generic_code, generic_text)
values(DEFAULT, 'MANDATORY_HEADER_ELEMENT_MISSING_ERROR', 'MGW-999902', 'Request could not be satisfied at this time. Please re-try, if the problem persists then please contact the ATOS Help Desk.'); 

INSERT INTO acknowledgement(acknowledgement_id, acknowledgement_type, generic_code, generic_text)
values(DEFAULT, 'MESSAGE_HEADER_VALIDATION_ERROR', 'MGW-999903', 'Request could not be satisfied at this time. Please re-try, if the problem persists then please contact the ATOS Help Desk.'); 

INSERT INTO acknowledgement(acknowledgement_id, acknowledgement_type, generic_code, generic_text)
values(DEFAULT, 'MESSAGE_TIMEOUT_ERROR', 'MGW-999904', 'Request could not be satisfied at this time. Please re-try, if the problem persists then please contact the ATOS Help Desk.'); 

INSERT INTO acknowledgement(acknowledgement_id, acknowledgement_type, generic_code, generic_text)
values(DEFAULT, 'DUPLICATE_MESSAGE_ERROR', 'MGW-999905', 'Request could not be satisfied at this time. Please re-try, if the problem persists then please contact the ATOS Help Desk.'); 


--
-- Recipient endpoint table data
--
INSERT INTO recipient_endpoint(recipient_endpoint_id, from_endpoint, from_url, to_endpoint, to_url, endpoint_url, endpoint_ping_url, endpoint_status, response_type, schema_id)
VALUES (DEFAULT, 'LIBRA', null, 'MAP', null, null, null, null, 'SYNC', 1);


--
-- Message map table data
--
INSERT INTO message_map(message_map_id, recipient_endpoint_id, action_type, libra_action_type, timeout, schema_id)
VALUES (DEFAULT, 1, 'sendCase', 'sendCase', 180, 1);

INSERT INTO message_map(message_map_id, recipient_endpoint_id, action_type, libra_action_type, timeout, schema_id)
VALUES (DEFAULT, 1, 'sendResults', 'sendResults', 180, 1);
