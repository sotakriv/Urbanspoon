from flask import Flask, request, redirect
import random

app = Flask(__name__)

# ============================================================
#  RESTAURANT DATA - Add your own here!
# ============================================================
RESTAURANTS = [
    {"id": 1, "name": "Joe's Pizza", "address": "7 Carmine St, New York, NY", "phone": "212-366-1182", "cuisine": "Pizza", "price_range": "1", "rating": 4.5, "lat": 40.7306, "lon": -74.0028, "description": "Classic NYC slice."},
    {"id": 2, "name": "Katz's Delicatessen", "address": "205 E Houston St, New York, NY", "phone": "212-254-2246", "cuisine": "Deli", "price_range": "2", "rating": 4.6, "lat": 40.7223, "lon": -73.9873, "description": "Legendary NYC deli since 1888."},
    {"id": 3, "name": "Xi'an Famous Foods", "address": "81 St Marks Pl, New York, NY", "phone": "212-786-2068", "cuisine": "Chinese", "price_range": "1", "rating": 4.4, "lat": 40.7275, "lon": -73.9857, "description": "Hand-ripped noodles and lamb burgers."},
    {"id": 4, "name": "Le Bernardin", "address": "155 W 51st St, New York, NY", "phone": "212-554-1515", "cuisine": "French", "price_range": "3", "rating": 4.9, "lat": 40.7617, "lon": -73.9817, "description": "World-renowned French seafood restaurant."},
    {"id": 5, "name": "Shake Shack", "address": "Madison Square Park, New York, NY", "phone": "212-889-6600", "cuisine": "Burgers", "price_range": "1", "rating": 4.3, "lat": 40.7410, "lon": -73.9883, "description": "The original Shake Shack location."},
]

PLIST_HEADER = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0">'
PLIST_FOOTER = '</plist>'
PLIST_CT = {'Content-Type': 'application/x-plist'}

def plist(content):
    return PLIST_HEADER + content + PLIST_FOOTER, 200, PLIST_CT

def restaurant_plist(r):
    return (
        '<dict>'
        '<key>id</key><integer>' + str(r["id"]) + '</integer>'
        '<key>name</key><string>' + r["name"] + '</string>'
        '<key>address</key><string>' + r["address"] + '</string>'
        '<key>phone</key><string>' + r["phone"] + '</string>'
        '<key>cuisine</key><string>' + r["cuisine"] + '</string>'
        '<key>rating</key><real>' + str(r["rating"]) + '</real>'
        '<key>lat</key><real>' + str(r["lat"]) + '</real>'
        '<key>lon</key><real>' + str(r["lon"]) + '</real>'
        '<key>description</key><string>' + r["description"] + '</string>'
        '<key>thumb_url</key><string></string>'
        '<key>url</key><string>http://www.urbanspoon.com/m/r/' + str(r["id"]) + '/restaurant</string>'
        '<key>mobile_url</key><string>http://www.urbanspoon.com/m/r/' + str(r["id"]) + '/restaurant</string>'
        '<key>review_count</key><integer>42</integer>'
        '<key>open_now</key><true/>'
        '<key>price_range</key><string>' + r["price_range"] + '</string>'
        '</dict>'
    )

@app.route("/aap.do", methods=["GET", "POST"])
def flurry():
    return plist('<dict><key>status</key><string>ok</string></dict>')

@app.route("/aas.do", methods=["GET", "POST"])
def flurry2():
    return plist('<dict><key>status</key><string>ok</string></dict>')

@app.route("/api/ihello")
def ihello():
    print("[ihello]")
    return plist(
        '<dict>'
        '<key>status</key><string>ok</string>'
        '<key>version</key><integer>14</integer>'
        '<key>city</key><string>New York</string>'
        '<key>country</key><string>US</string>'
        '<key>within</key><integer>1000</integer>'
        '<key>lat</key><real>40.7128</real>'
        '<key>lon</key><real>-74.0060</real>'
        '<key>neighborhoods</key><array>'
        '<dict><key>obj_id</key><integer>0</integer><key>title</key><string>Any Area</string></dict>'
        '<dict><key>obj_id</key><integer>1</integer><key>title</key><string>Manhattan</string></dict>'
        '<dict><key>obj_id</key><integer>2</integer><key>title</key><string>Brooklyn</string></dict>'
        '<dict><key>obj_id</key><integer>3</integer><key>title</key><string>Queens</string></dict>'
        '</array>'
        '<key>cuisines</key><array>'
        '<dict><key>obj_id</key><integer>0</integer><key>title</key><string>Any Food</string></dict>'
        '<dict><key>obj_id</key><integer>1</integer><key>title</key><string>American</string></dict>'
        '<dict><key>obj_id</key><integer>2</integer><key>title</key><string>Pizza</string></dict>'
        '<dict><key>obj_id</key><integer>3</integer><key>title</key><string>Chinese</string></dict>'
        '<dict><key>obj_id</key><integer>4</integer><key>title</key><string>French</string></dict>'
        '<dict><key>obj_id</key><integer>5</integer><key>title</key><string>Burgers</string></dict>'
        '<dict><key>obj_id</key><integer>6</integer><key>title</key><string>Deli</string></dict>'
        '</array>'
        '<key>prices</key><array>'
        '<dict><key>obj_id</key><integer>0</integer><key>title</key><string>Any Price</string></dict>'
        '<dict><key>obj_id</key><integer>1</integer><key>title</key><string>$</string></dict>'
        '<dict><key>obj_id</key><integer>2</integer><key>title</key><string>$$</string></dict>'
        '<dict><key>obj_id</key><integer>3</integer><key>title</key><string>$$$</string></dict>'
        '</array>'
        '</dict>'
    )

@app.route("/api/ispin")
def ispin():
    print("[ispin]")
    r = random.choice(RESTAURANTS)
    return plist(
        '<dict>'
        '<key>status</key><string>ok</string>'
        '<key>obj_id</key><integer>' + str(r["id"]) + '</integer>'
        '<key>title</key><string>' + r["name"] + '</string>'
        '<key>address</key><string>' + r["address"] + '</string>'
        '<key>cuisine</key><string>' + r["cuisine"] + '</string>'
        '<key>cuisine_id</key><integer>1</integer>'
        '<key>neighborhood_id</key><integer>1</integer>'
        '<key>price_id</key><integer>1</integer>'
        '<key>price</key><string>' + r["price_range"] + '</string>'
        '<key>distance_miles</key><real>0.3</real>'
        '<key>lat</key><real>' + str(r["lat"]) + '</real>'
        '<key>lon</key><real>' + str(r["lon"]) + '</real>'
        '<key>url</key><string>http://www.urbanspoon.com/m/r/' + str(r["id"]) + '/restaurant</string>'
        '<key>restaurant</key>' + restaurant_plist(r) +
        '</dict>'
    )

@app.route("/m/r/<int:rid>/restaurant")
@app.route("/r/<int:rid>/restaurant")
def restaurant_page(rid):
    print("[restaurant_page] " + str(rid))
    r = next((x for x in RESTAURANTS if x["id"] == rid), RESTAURANTS[0])
    return '<html><body><h1>' + r["name"] + '</h1><p>' + r["address"] + '</p><p>' + r["phone"] + '</p><p>' + r["cuisine"] + '</p></body></html>'

@app.route("/api/lists")
def lists():
    return plist('<dict><key>status</key><string>ok</string><key>lists</key><array/><key>neighborhoods</key><array/><key>cuisines</key><array/><key>price_ranges</key><array/></dict>')

@app.route("/api/icheck_auth")
def icheck_auth():
    return plist('<dict><key>status</key><string>ok</string><key>authenticated</key><true/><key>user</key><dict><key>id</key><integer>1</integer><key>name</key><string>Local User</string><key>email</key><string>user@local.com</string></dict></dict>')

@app.route("/api/ad_zones")
def ad_zones():
    return plist('<dict><key>status</key><string>ok</string><key>ads</key><array/></dict>')

@app.route("/api/ad_spin")
def ad_spin():
    return plist('<dict><key>status</key><string>ok</string><key>ads</key><array/></dict>')

@app.route("/api/itott")
def itott():
    return plist('<dict><key>status</key><string>ok</string></dict>')

@app.route("/api/grid_rows")
def grid_rows():
    rows = ''.join(['<dict><key>type</key><string>restaurant</string><key>restaurant</key>' + restaurant_plist(r) + '</dict>' for r in RESTAURANTS])
    return plist('<dict><key>status</key><string>ok</string><key>rows</key><array>' + rows + '</array></dict>')

@app.route("/api/isearch")
def isearch():
    query = request.args.get("q", "").lower()
    results = [r for r in RESTAURANTS if query in r["name"].lower()] if query else RESTAURANTS
    items = ''.join([restaurant_plist(r) for r in results])
    return plist('<dict><key>status</key><string>ok</string><key>restaurants</key><array>' + items + '</array></dict>')

@app.route("/api/inearme")
def inearme():
    items = ''.join([restaurant_plist(r) for r in RESTAURANTS])
    return plist('<dict><key>status</key><string>ok</string><key>restaurants</key><array>' + items + '</array></dict>')

@app.route("/api/icity")
def icity():
    return plist('<dict><key>status</key><string>ok</string><key>cities</key><array><dict><key>id</key><integer>1</integer><key>name</key><string>New York</string><key>lat</key><real>40.7128</real><key>lon</key><real>-74.0060</real><key>country</key><string>US</string></dict></array></dict>')

@app.route("/m/u/tip")
def tip():
    return '<html><body>Shake to spin!</body></html>'

@app.route("/api/iredirect/friends")
def friends():
    return plist('<dict><key>status</key><string>ok</string><key>friends</key><array/></dict>')

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    print("[catch_all] /" + path)
    return plist('<dict><key>status</key><string>ok</string></dict>')

if __name__ == "__main__":
    print("=" * 50)
    print("  Urbanspoon Local Server")
    print("  Running on http://0.0.0.0:80")
    print("=" * 50)
    app.run(host="0.0.0.0", port=80, debug=True)
