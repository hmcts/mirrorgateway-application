
--
-- recipient end point table not null constraint on the primary key
--
ALTER TABLE recipient_endpoint         
ADD CONSTRAINT re_rei_nn 
CHECK (recipient_endpoint_id IS NOT NULL);

--
-- message map table not null constraint on the primary key
--
ALTER TABLE message_map              
ADD CONSTRAINT mm_mmi_nn  
CHECK (message_map_id IS NOT NULL);

--
-- message audit table not null constraint on the primary key
--
ALTER TABLE message_audit                
ADD CONSTRAINT ma_mai_nn  
CHECK (message_audit_id IS NOT NULL);

--
-- message status table not null constraint on the primary key
--
ALTER TABLE message_status                
ADD CONSTRAINT bc_msg_st  
CHECK (message_status_id IS NOT NULL);

--
-- schema details table not null constraint on the primary key
--
ALTER TABLE schema_details                
ADD CONSTRAINT sd_si_nn  
CHECK (schema_id IS NOT NULL);

--
-- request operation table not null constraint on the primary key
--
ALTER TABLE request_operation                
ADD CONSTRAINT ro_roi_nn  
CHECK (request_operation_id IS NOT NULL);

--
-- acknowledgement table not null constraint on the primary key
--
ALTER TABLE acknowledgement                
ADD CONSTRAINT a_ai_nn  
CHECK (acknowledgement_id IS NOT NULL);
