#uvicorn main:app --host 0.0.0.0 --port 8000 --reload
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import db_helper
import generic_helper
app = FastAPI()

inprogress_orders = {}
@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()
        print("📦 Payload received:", payload)

        intent = payload['queryResult']['intent']['displayName']
        print("🎯 Intent Name Received:", intent)
        parameters = payload['queryResult'].get('parameters', {})
        output_contexts = payload['queryResult']['outputContexts']
        session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

        # fallback if empty parameters
        if not parameters and output_contexts:
            for context in output_contexts:
                if 'parameters' in context:
                    parameters = context['parameters']
                    break

        intent_handler_dict = {
            'order.add': add_to_order,
            'order.remove': remove_from_order,
            'order.complete': complete_order,
            'track.byorderid': track_order,
            'reserve.table': reserve_table
        }

        if intent in intent_handler_dict:
            return intent_handler_dict[intent](parameters, session_id)
        else:
            return JSONResponse(content={"fulfillmentText": "Sorry, I didn't understand your request."})

    except Exception as e:
        print("❌ ERROR:", str(e))
        traceback.print_exc()
        return JSONResponse(content={"fulfillmentText": "Internal server error occurred."})




def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    # Insert individual items along with quantity in orders table
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1

    # Now insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order id # {order_id}. " \
                               f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def reserve_table(parameters: dict, session_id: str):
    try:
        number_of_people = parameters.get("noofpeople")  # updated from "number"
        time_param = parameters.get("date-time")         # updated from "time"

        if not number_of_people or not time_param:
            return JSONResponse(content={
                "fulfillmentText": "Could you please provide both the time and number of people for the reservation?"
            })

        # If Dialogflow sends these as lists (which it often does), extract first element
        if isinstance(time_param, list):
            time_param = time_param[0]

        number_of_people = int(number_of_people)

        table_id = db_helper.insert_reservation(time_param, number_of_people)

        if table_id == -1:
            fulfillment_text = "Sorry, I couldn't book the table right now due to a technical issue."
        else:
            fulfillment_text = (
                f"✅ Your table has been reserved! Table number is #{table_id} "
                f"for {number_of_people} people at {time_param}."
            )

    except Exception as e:
        print("❌ ERROR in reserve_table():", str(e))
        fulfillment_text = "Something went wrong while booking your table. Please try again."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})
