#!/usr/bin/env python
# encoding: utf-8
import json
import redis
import time
import math
from flask import Flask, request, jsonify

app = Flask(__name__)
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
fee = 10
minutes_in_hour = 15
@app.route('/', methods=['GET'])
def heath_check():
	return jsonify({'status':'alive'})

@app.route('/entry', methods=['POST'])
def enter_parking():
	entry_timestamp = time.time()
	args = request.args
	plate = args.get("plate")
	parking_lot = args.get("parkingLot")
	if (plate is not None and len(plate.strip())) and (parking_lot is not None  and len(parking_lot.strip())):
		entry_data = json.dumps(
		{'enter_timestamp': entry_timestamp, 'plate_number': plate, 'parking_lot': parking_lot})
		ticket_id = f"{plate}_{parking_lot}" #car plate & parkinglot combination is universally unique 
		
		if redis_db.exists(ticket_id):
			return jsonify({'error': 'car is already parking in the requests parking lot.'})

		redis_db.set(ticket_id, entry_data)

		return ticket_id
	else:
		return jsonify({'error': 'invalid request please verify your parameters.'})


@app.route('/exit', methods=['POST'])
def exit_parking():
	exit_timestamp = time.time()
	ticket_id = request.args.get("ticketId")
	
	if ticket_id is None or (not len(ticket_id.strip())):
		return jsonify({'error': 'invalid request please verify your parameters.'})
	
	parking_data = redis_db.get(ticket_id)
	redis_db.delete(ticket_id)
	
	if parking_data is None or (not len(parking_data.strip())):
		return jsonify({'error':'ticket id not found.'})

	parking_info = json.loads(parking_data)
	entry_timestamp = parking_info['enter_timestamp']
	plate = parking_info['plate_number']
	parking_lot = parking_info['parking_lot']
	total_seconds = exit_timestamp - entry_timestamp
	total_minutes = total_seconds / 60
	charge_units = math.ceil(total_minutes / minutes_in_hour)
	total_charge = charge_units * fee
	result = {'plate' : plate, 'total_parking_time_in_minutes':total_minutes, 'parking_lot' : parking_lot, 'total_charge':total_charge}
	
	return jsonify(result)

