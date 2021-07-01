import { quadtree } from "https://cdn.skypack.dev/d3-quadtree@3";

const icon = L.icon({
	iconUrl: "/marker.png",
	iconSize: [10, 10], // size of the icon
});

function loadMap(apikey) {
	const mymap = L.map("mapid").setView([-37.8, 145.3], 10);

	L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${apikey}`, {
		attribution:
			'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: "mapbox/streets-v11",
		tileSize: 512,
		zoomOffset: -1,
		accessToken: apikey,
	}).addTo(mymap);
	return mymap;
}

async function loadData() {
	const req = await fetch("/data");
	const data = await req.json();
	const cleanedData = data
		.map((val, index, arr) => {
			if (val.lat !== 0.0) {
				return val;
			}
		})
		.filter(Boolean);
	return cleanedData;
}

async function getApiKey() {
	const req = await fetch("/api-key");
	const data = await req.json();
	return data.key;
}

function loadMarkers(data) {
	const markers = L.markerClusterGroup();
	for (const node of data) {
		const marker = L.marker([node.lat, node.lon], { icon: icon });
		marker.bindPopup(`lat: ${node.lat}<br/>lon: ${node.lon}<br/>path:${node.filename}`);
		markers.addLayer(marker);
	}
	return markers;
}

function x(d) {
	return d.lat;
}

function y(d) {
	return d.lon;
}

function search(quadtree, xmin, ymin, xmax, ymax) {
	const results = [];
	quadtree.visit((node, x1, y1, x2, y2) => {
		if (!node.length) {
			do {
				const x = node.data.lat;
				const y = node.data.lon;
				if (x >= xmin && x < xmax && y >= ymin && y < ymax) {
					results.push(node.data);
				}
			} while ((node = node.next));
		}
		return x1 >= xmax || y1 >= ymax || x2 < xmin || y2 < ymin;
	});
	return results;
}

function handleMapChange(event, tree) {
	const bounds = event.sourceTarget.getBounds();
	const markersInBounds = getMarkersInsideBounds(bounds, tree);
	const target = document.getElementById("boundsList");

	// remove old nodes
	const childrenToRemove = target.querySelectorAll("div");
	for (const n of childrenToRemove) n.remove();

	// add new nodes
	for (const node of markersInBounds) {
		const newNode = document.createElement("div");
		const newNodeSpan = document.createElement("span");
		newNodeSpan.innerHTML = node.filename;
		newNode.appendChild(newNodeSpan);
		target.appendChild(newNode);
	}
}

async function app() {
	console.log("running");
	const apiKey = await getApiKey();
	const mymap = loadMap(apiKey);
	const data = await loadData();
	console.log(data);

	const markers = loadMarkers(data);
	mymap.addLayer(markers);

	const tree = quadtree().x(x).y(y).addAll(data);

	const handleMapChangeWithData = (e) => handleMapChange(e, tree);
	mymap.on("moveend", handleMapChangeWithData);
}

document.addEventListener("DOMContentLoaded", app);

// ! Don't need these functions anymore because i found the marker cluster plugin
// ! https://docs.mapbox.com/mapbox.js/example/v1.0.0/leaflet-markercluster/

function getMarkersInsideBounds(bounds, tree) {
	// do not question the holy coordinates that work
	const xmin = bounds._northEast.lat;
	const ymin = bounds._southWest.lng;
	const xmax = bounds._southWest.lat;
	const ymax = bounds._northEast.lng;

	const result = search(tree, xmax, ymin, xmin, ymax);

	console.log(result);
	return result;
}

// ! DEPRECATED fallback for no cubetree method
function deprecatedGetMarkersInsideBounds(bounds, tree) {
	let count = 0;
	const markersInBounds = [];
	for (const node of markers) {
		// max 300 things for performance reasons
		if (count > 300) break;
		if (
			node.lat < bounds._northEast.lat &&
			node.lon < bounds._northEast.lng &&
			node.lat > bounds._southWest.lat &&
			node.lon > bounds._southWest.lng
		) {
			count++;
			markersInBounds.push(node);
		}
	}
	console.log(count);
	return markersInBounds;
}
