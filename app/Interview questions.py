“What is Depends in FastAPI?
 answer:
     Depends is used for dependency injection. It allows reusable logic like authentication, database sessions, and validations to be executed before the endpoint runs.”
 
 
 What is BaseSettings?

Answer:

“BaseSettings is used to manage environment variables in a structured and validated way. It helps separate configuration from code and improves security.”


Why create session per request?

Answer:

“Each request gets its own database session to ensure isolation, thread safety, and proper transaction handling. Sessions are lightweight and use connection pooling internally, so performance is not impacted.” 

Why separate request and response schemas?

Answer:

“To ensure data validation, security, and controlled API responses. Request schemas validate input, while response schemas prevent exposing sensitive data.”   

What is CryptContext?

“CryptContext from passlib is used to manage password hashing and verification. It supports multiple hashing schemes and allows safe password storage and validation.”

What is from_attributes in Pydantic?

“It allows Pydantic models to read data from ORM objects instead of dictionaries, enabling seamless serialization in FastAPI.”

How do you implement RBAC in FastAPI?

Answer:

“Using dependency injection, I created a reusable role-checking function that validates user roles before allowing access to endpoints.”


How do you improve API performance?

Answer:

“By introducing Redis caching to store frequently accessed data and reduce database load.”
     
     
How do you handle long-running tasks?

“We use background tasks for lightweight operations and tools like Celery for heavy asynchronous processing.”


How do you protect APIs from abuse?

“By implementing rate limiting using Redis-backed mechanisms like SlowAPI to restrict request frequency per user or IP.”
     