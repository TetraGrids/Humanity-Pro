import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

const stage = document.querySelector(".stage");
const canvas = document.getElementById("view");
const rail = document.getElementById("rail");
const panel = document.getElementById("panel");
const meta = document.getElementById("meta");
const KIND_ORDER = ["program", "contract", "plugin", "action", "table", "notify", "option", "interface", "class", "file"];
const KIND_LABEL = {
  program: "Programs",
  contract: "Contracts",
  plugin: "Plugins",
  action: "Actions",
  table: "Tables",
  notify: "Notifies",
  option: "Options",
  interface: "Interfaces",
  class: "Classes",
  file: "Files",
};
const LAYOUT = {
  programs: { center: [0, 3, -15], radius: 5 },
  contracts: { center: [-16, -1, 7], radius: 7.2 },
  plugins: { center: [16, -1, 7], radius: 8.4 },
};

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setClearColor(0x050705, 1);

const scene = new THREE.Scene();
scene.fog = new THREE.Fog(0x050705, 36, 92);
const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 200);
camera.position.set(0, 12, 36);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.target.set(0, 0, 0);
controls.maxDistance = 90;
controls.minDistance = 6;

scene.add(new THREE.AmbientLight(0xf4f7f4, 0.35));
const key = new THREE.DirectionalLight(0xf4f7f4, 1.1);
key.position.set(8, 18, 12);
scene.add(key);
const glow = new THREE.PointLight(0x22c55e, 8, 40);
glow.position.set(0, 4, 6);
scene.add(glow);

const world = new THREE.Group();
scene.add(world);
const grid = new THREE.GridHelper(70, 28, 0x16331f, 0x0c1610);
grid.position.y = -10;
scene.add(grid);

const meshes = new Map();
const focus = new THREE.Vector3();
let catalog = null;
let byId = new Map();
let selected = "humanity-pro";
let hovered = null;
let seen = "";
let focusUntil = 0;
let dragging = false;

function shell(index, count, radius) {
  if (count === 1) return new THREE.Vector3();
  const phi = Math.acos(1 - (2 * (index + 0.5)) / count);
  const theta = Math.PI * (1 + Math.sqrt(5)) * index;
  return new THREE.Vector3(
    radius * Math.sin(phi) * Math.cos(theta),
    radius * Math.cos(phi) * 0.72,
    radius * Math.sin(phi) * Math.sin(theta),
  );
}

function labelTexture(text, color) {
  const context = document.createElement("canvas").getContext("2d");
  context.font = "500 32px Jost, sans-serif";
  const width = Math.ceil(context.measureText(text).width) + 24;
  context.canvas.width = width;
  context.canvas.height = 48;
  context.font = "500 32px Jost, sans-serif";
  context.fillStyle = color;
  context.fillText(text, 12, 34);
  const texture = new THREE.CanvasTexture(context.canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return { texture, width };
}

function makeLabel(text, color, scale) {
  const drawn = labelTexture(text, color);
  const sprite = new THREE.Sprite(
    new THREE.SpriteMaterial({ map: drawn.texture, transparent: true, depthWrite: false }),
  );
  sprite.scale.set(drawn.width * scale, 48 * scale, 1);
  sprite.userData.texture = drawn.texture;
  return sprite;
}

function dispose(object) {
  object.traverse((child) => {
    child.geometry?.dispose();
    child.userData.texture?.dispose();
    const materials = child.material ? [].concat(child.material) : [];
    materials.forEach((material) => {
      material.map?.dispose();
      material.dispose();
    });
  });
}

function tetra(color, base) {
  const geometry = new THREE.TetrahedronGeometry(0.72, 0);
  const mesh = new THREE.Mesh(
    geometry,
    new THREE.MeshStandardMaterial({
      color: 0x101610,
      emissive: new THREE.Color(color),
      emissiveIntensity: 0.12,
      roughness: 0.45,
      metalness: 0.35,
    }),
  );
  mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geometry), new THREE.LineBasicMaterial({ color })));
  const hit = new THREE.Mesh(
    new THREE.SphereGeometry(1.35, 8, 8),
    new THREE.MeshBasicMaterial({ visible: false }),
  );
  mesh.add(hit);
  mesh.userData.color = color;
  mesh.userData.base = base;
  return mesh;
}

function line(from, to, color) {
  const geometry = new THREE.BufferGeometry().setFromPoints([from, to]);
  return new THREE.Line(geometry, new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.45 }));
}

function buildScene(data) {
  while (world.children.length) {
    dispose(world.children[0]);
    world.remove(world.children[0]);
  }
  meshes.clear();
  const rootMesh = tetra("#22c55e", 2.15);
  rootMesh.userData.id = data.root.id;
  rootMesh.position.set(0, 0, 0);
  world.add(rootMesh);
  meshes.set(data.root.id, rootMesh);
  const rootLabel = makeLabel(data.root.name, "#f4f7f4", 0.018);
  rootLabel.position.set(0, 2.3, 0);
  world.add(rootLabel);

  for (const group of data.groups) {
    const layout = LAYOUT[group.id];
    const center = new THREE.Vector3(...layout.center);
    const cluster = new THREE.Group();
    cluster.position.copy(center);
    world.add(cluster);
    world.add(line(new THREE.Vector3(), center, group.color));
    const title = makeLabel(group.name, group.color, 0.016);
    title.position.copy(center.clone().normalize().multiplyScalar(layout.radius + 2.6));
    cluster.add(title);
    group.nodes.forEach((node, index) => {
      const mesh = tetra(group.color, 1);
      mesh.userData.id = node.id;
      mesh.position.copy(shell(index, group.nodes.length, layout.radius));
      const name = makeLabel(node.name, "#f4f7f4", 0.012);
      name.position.set(0, 1.2, 0);
      name.visible = false;
      name.userData.pixelWidth = name.scale.x / 0.012;
      mesh.add(name);
      mesh.userData.label = name;
      cluster.add(mesh);
      cluster.add(line(new THREE.Vector3(), mesh.position, group.color));
      meshes.set(node.id, mesh);
    });
  }
  paint();
}

function connected(id) {
  const ids = new Set();
  const node = byId.get(id);
  if (!node || !catalog || id === catalog.root.id) return ids;
  for (const item of node.contains || []) {
    if (item.id && byId.has(item.id) && item.id !== catalog.root.id) ids.add(item.id);
  }
  for (const other of byId.values()) {
    if (other.id === catalog.root.id) continue;
    if ((other.contains || []).some((item) => item.id === id)) ids.add(other.id);
  }
  ids.delete(id);
  return ids;
}

function paint() {
  const near = connected(selected);
  for (const [id, mesh] of meshes) {
    const on = id === selected;
    const scale = mesh.userData.base * (on ? 1.28 : 1);
    mesh.material.emissiveIntensity = on ? 0.85 : near.has(id) ? 0.28 : 0.08;
    mesh.children[0].material.color.set(on ? 0xffe566 : mesh.userData.color);
    mesh.scale.setScalar(scale);
    if (mesh.userData.label) {
      mesh.userData.label.visible = on || id === hovered || near.has(id);
      const k = 0.012 / scale;
      mesh.userData.label.scale.set(mesh.userData.label.userData.pixelWidth * k, 48 * k, 1);
    }
  }
}

function button(parent, className) {
  const el = document.createElement("button");
  el.type = "button";
  if (className) el.className = className;
  parent.appendChild(el);
  return el;
}

function renderRail(data) {
  rail.replaceChildren();
  const home = button(rail);
  home.id = "nav-humanity-pro";
  home.textContent = data.root.name;
  home.addEventListener("click", () => select(data.root.id));
  for (const group of data.groups) {
    const heading = document.createElement("div");
    heading.className = "group-label";
    heading.textContent = group.name;
    rail.appendChild(heading);
    for (const node of group.nodes) {
      const item = button(rail);
      item.id = `nav-${node.id}`;
      item.textContent = node.name;
      item.addEventListener("click", () => select(node.id));
    }
  }
  markRail();
}

function markRail() {
  for (const item of rail.querySelectorAll("button")) item.classList.toggle("on", item.id === `nav-${selected}`);
  document.getElementById(`nav-${selected}`)?.scrollIntoView({ block: "nearest" });
}

function renderPanel(id) {
  const node = byId.get(id);
  panel.replaceChildren();
  if (!node) return;
  const kicker = document.createElement("div");
  kicker.className = "kicker";
  kicker.textContent = node.kind;
  const title = document.createElement("h1");
  title.textContent = node.name;
  const path = document.createElement("p");
  path.className = "path";
  path.textContent = node.path || "repository root";
  const summary = document.createElement("p");
  summary.className = "summary";
  summary.textContent = node.summary;
  panel.append(kicker, title, path, summary);
  const buckets = new Map();
  for (const item of node.contains || []) {
    if (!buckets.has(item.kind)) buckets.set(item.kind, []);
    buckets.get(item.kind).push(item);
  }
  const kinds = [...buckets.keys()].sort((a, b) => KIND_ORDER.indexOf(a) - KIND_ORDER.indexOf(b));
  if (!kinds.length) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "Nothing nested in this component.";
    panel.append(empty);
    return;
  }
  for (const kind of kinds) {
    const bucket = document.createElement("section");
    bucket.className = "bucket";
    const heading = document.createElement("h2");
    heading.textContent = `${KIND_LABEL[kind] || kind} ${buckets.get(kind).length}`;
    const list = document.createElement("ul");
    list.className = "contains";
    for (const item of buckets.get(kind)) {
      const row = document.createElement("li");
      const control = button(row);
      control.textContent = item.name;
      if (item.id && byId.has(item.id)) {
        control.dataset.go = item.id;
        control.addEventListener("click", () => select(item.id));
      }
      const about = document.createElement("p");
      about.textContent = item.summary;
      row.append(about);
      list.append(row);
    }
    bucket.append(heading, list);
    panel.append(bucket);
  }
}

function select(id) {
  if (!byId.has(id)) return;
  selected = id;
  const mesh = meshes.get(id);
  if (mesh) {
    mesh.getWorldPosition(focus);
    focusUntil = performance.now() + 800;
  }
  paint();
  markRail();
  renderPanel(id);
}

function apply(data) {
  catalog = data;
  byId = new Map([[data.root.id, data.root]]);
  for (const group of data.groups) for (const node of group.nodes) byId.set(node.id, node);
  const count = byId.size - 1;
  meta.textContent = `${count} components`;
  buildScene(data);
  renderRail(data);
  if (!byId.has(selected)) selected = data.root.id;
  select(selected);
}

async function pull() {
  const response = await fetch("components.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`components.json ${response.status}`);
  const text = await response.text();
  if (text === seen) return;
  seen = text;
  apply(JSON.parse(text));
}

window.updateComponents = (data) => {
  seen = JSON.stringify(data);
  apply(data);
};

const pointer = new THREE.Vector2();
const ray = new THREE.Raycaster();
let down = null;

function pick(event) {
  const rect = canvas.getBoundingClientRect();
  pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  ray.setFromCamera(pointer, camera);
  const hits = ray.intersectObject(world, true);
  for (const hit of hits) {
    let object = hit.object;
    while (object) {
      if (object.userData.id) return object.userData.id;
      object = object.parent;
    }
  }
  return null;
}

canvas.addEventListener("pointerdown", (event) => {
  dragging = true;
  down = [event.clientX, event.clientY];
});
window.addEventListener("pointerup", (event) => {
  dragging = false;
  if (!down) return;
  const moved = (event.clientX - down[0]) ** 2 + (event.clientY - down[1]) ** 2;
  down = null;
  if (moved > 144) return;
  const id = pick(event);
  if (id) select(id);
});
canvas.addEventListener("pointermove", (event) => {
  const id = pick(event);
  canvas.style.cursor = id ? "pointer" : "";
  if (id !== hovered) {
    hovered = id;
    paint();
  }
});

function resize() {
  const width = stage.clientWidth;
  const height = stage.clientHeight;
  if (!width || !height) return;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage);

function frame(now) {
  if (now < focusUntil) controls.target.lerp(focus, 0.14);
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(frame);
}

pull()
  .then(() => {
    if (document.fonts?.ready) return document.fonts.ready.then(() => catalog && buildScene(catalog));
  })
  .catch((error) => {
    panel.textContent = `${error.message}. Run python3 web/components/serve.py`;
  });
setInterval(() => pull().catch(() => {}), 2000);
requestAnimationFrame(frame);
resize();
