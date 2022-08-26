
CREATE TABLE recipient_endpoint
(recipient_endpoint_id       SERIAL                
,from_endpoint               VARCHAR(20)         
,from_url                    VARCHAR(200)       
,to_endpoint                 VARCHAR(20)        
,to_url                      VARCHAR(200)       
,endpoint_url                VARCHAR(255)
,endpoint_ping_url           VARCHAR(255)
,endpoint_status             VARCHAR(1) DEFAULT 'A'       
,response_type               VARCHAR(5)            
,schema_id                   INTEGER               
,updated_date                TIMESTAMP           
,version_number              INTEGER DEFAULT 0    
) ;

COMMENT ON COLUMN recipient_endpoint.recipient_endpoint_id IS 'Sequence generated primary key';
COMMENT ON COLUMN recipient_endpoint.from_endpoint IS 'Source application name (i.e. LAA or Libra)';
COMMENT ON COLUMN recipient_endpoint.from_url IS 'Source application addressing url';
COMMENT ON COLUMN recipient_endpoint.to_endpoint IS 'Target application name';
COMMENT ON COLUMN recipient_endpoint.to_url IS 'Target application addressing url';
COMMENT ON COLUMN recipient_endpoint.endpoint_url IS 'Endpoint URL';
COMMENT ON COLUMN recipient_endpoint.endpoint_ping_url IS 'Endpoint ping URL';
COMMENT ON COLUMN recipient_endpoint.endpoint_status IS 'Status A ctive or I nactive';
COMMENT ON COLUMN recipient_endpoint.response_type IS 'Expected result types in answer to a request SYNC or ASYNC';
COMMENT ON COLUMN recipient_endpoint.schema_id IS 'Schema version for request to validated against';
COMMENT ON COLUMN recipient_endpoint.updated_date IS 'Timestamp according to when the record was last updated (UPDATE)';
COMMENT ON COLUMN recipient_endpoint.version_number IS 'hiberate versioning column';


CREATE TABLE message_map
(message_map_id              SERIAL                
,recipient_endpoint_id       INTEGER                
,action_type                 VARCHAR(200)
,libra_action_type           VARCHAR(200)
,timeout                     INTEGER                
,schema_id                   INTEGER                
,updated_date                TIMESTAMP          
,version_number              INTEGER DEFAULT 0    
) ;

COMMENT ON COLUMN message_map.message_map_id IS 'Sequence generated primary key';
COMMENT ON COLUMN message_map.recipient_endpoint_id IS 'Foreign Key to Recipient_endpoint table';
COMMENT ON COLUMN message_map.action_type IS 'Allowable action from the request originating source';
COMMENT ON COLUMN message_map.libra_action_type IS 'Allowable libra action from the request originating source';
COMMENT ON COLUMN message_map.timeout IS 'Time to wait for a response, in seconds';
COMMENT ON COLUMN message_map.schema_id IS 'Schema version to be used by request to be validated';
COMMENT ON COLUMN message_map.updated_date IS 'Timestamp according to when the record was last updated (UPDATE)';
COMMENT ON COLUMN message_map.version_number IS 'hiberate versioning column';


CREATE TABLE message_audit
(message_audit_id            SERIAL               
,from_endpoint               VARCHAR(20)        
,to_endpoint                 VARCHAR(20)        
,action_type                 VARCHAR(200)        
,message_uuid                VARCHAR(60)       
,message_status_id           INTEGER                
,message_content             TEXT               
,updated_date                TIMESTAMP           
,version_number              INTEGER DEFAULT 0    
) ;

COMMENT ON COLUMN message_audit.message_audit_id IS 'Sequence generated primary key';
COMMENT ON COLUMN message_audit.from_endpoint IS 'Request originating source endpoint (i.e. LAA or Libra)';
COMMENT ON COLUMN message_audit.to_endpoint IS 'Request destination endpoint (i.e. LAA or Libra)';
COMMENT ON COLUMN message_audit.action_type IS 'Requested action with-in source originating request';
COMMENT ON COLUMN message_audit.message_uuid IS 'Unique identifier to distinguish each message';
COMMENT ON COLUMN message_audit.message_status_id IS 'Current state of request (FK to Message_status table';
COMMENT ON COLUMN message_audit.message_content IS 'raw message content';
COMMENT ON COLUMN message_audit.updated_date IS 'Time record when the request received by Gateway';
COMMENT ON COLUMN message_audit.version_number IS 'hiberate versioning column';


CREATE TABLE message_status 
(message_status_id           SERIAL               
,message_status              VARCHAR(40)        
,version_number              INTEGER DEFAULT 0   
) ; 

COMMENT ON COLUMN message_status.message_status_id IS 'Sequence generated primary key';
COMMENT ON COLUMN message_status.message_status IS 'Processed status of each message, I.e. RECEIVED, SCHEMA ERROR, QUEUED';
COMMENT ON COLUMN message_status.version_number IS 'hiberate versioning column';


CREATE TABLE schema_details
(schema_id                   SERIAL            
,schema_version              VARCHAR(20)        
--,schema_content            TEXT                
,version_number              INTEGER DEFAULT 0    
) ;

COMMENT ON COLUMN schema_details.schema_id IS 'Sequence generated primary key';
COMMENT ON COLUMN schema_details.schema_version IS 'Version of xsd used to validate incoming request';
COMMENT ON COLUMN schema_details.version_number IS 'hiberate versioning column';


CREATE TABLE request_operation
(request_operation_id      SERIAL      
,request_type              VARCHAR(200)         
,operation                 VARCHAR(200)         
) ;

COMMENT ON COLUMN request_operation.request_operation_id IS 'Sequence generated primary key';
COMMENT ON COLUMN request_operation.request_type IS 'Request class name' ;
COMMENT ON COLUMN request_operation.operation IS 'Operation name to invoke on the web service';


CREATE TABLE acknowledgement
(acknowledgement_id      SERIAL
,acknowledgement_type    VARCHAR(50)    NOT NULL
,generic_code            VARCHAR(50)    NOT NULL
,generic_text            VARCHAR(255)   NOT NULL
) ;
