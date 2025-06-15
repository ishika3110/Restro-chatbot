# Restro-chatbot

https://github.com/user-attachments/assets/c92b903a-983a-4346-9088-b0c9b38926c2

Built an intelligent, end-to-end restaurant chatbot system that enables users to interact seamlessly for food ordering, table reservations, order tracking, and customer support via natural language.  
🧠 NLP & Intent Handling: Integrated Dialogflow CX for intent detection (e.g., ordering, reservations, cancellations).  
🌐 Backend API: Developed a robust FastAPI webhook backend to handle dynamic user requests and interact with a MySQL database.  
🍽️ Order Management: Implemented backend logic to insert, update, and retrieve food orders, calculate total prices, and manage order status.  
📅 Table Reservation: Added support for handling reservations by number of people and time, with input validation.  
📊 Database Design: Designed a relational MySQL schema with tables like food_items, orders, and order_tracking, along with stored procedures and functions (get_price_for_item, insert_order_item, etc.).  
💬 Custom Web Chat UI: Developed a responsive HTML/CSS/JavaScript-based chatbot widget that integrates with Dialogflow using REST API and OAuth token handling.  
🛠️ Error Handling & Validation: Ensured robust handling of user input errors and backend database constraints (e.g., item availability, invalid quantities).  
🌐 Deployment Ready: Structured the project for future deployment to GCP / AWS, with OAuth token support and easy webhook configuration.  

🚀 Key Technologies:  
Dialogflow CX / ES (Natural Language Understanding)  
FastAPI (Python Web Framework)  
MySQL (Database & Stored Procedures)  
JavaScript / HTML / CSS (Frontend Chat Widget)  
OAuth 2.0 (Secure Token Integration)  
Git & GitHub for Version Control  

🧩 Live Features / Demo Suggestions (Optional):  
Try placing an order: “I want 2 plates of Chole Chawal”  
Reserve a table: “Book a table for 4 at 7 PM”  
Track order: “Where is my order?”  

If you have any queries regarding the project or need to know how to setup this email me at ishikaa.sharma3110@gmail.com
