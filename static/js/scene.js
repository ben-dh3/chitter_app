import * as THREE from 'https://cdn.jsdelivr.net/npm/three@v0.128.0/build/three.module.min.js';

async function loadShader(url) {
    const response = await fetch(url);
    return response.text();
}

(async function init() {
    const canvas = document.getElementById('threejs-canvas');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#000000');

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const mainRenderTarget = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight);
    const backRenderTarget = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight);

    const vertexShader = await loadShader('/static/shaders/vertexShader.glsl');
    const fragmentShader = await loadShader('/static/shaders/fragmentShader.glsl');

    const shaderMaterial = new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms: {
            uTexture: { value: null },
            uIorR: { value: 1.15 },
            uIorY: { value: 1.16 },
            uIorG: { value: 1.18 },
            uIorC: { value: 1.22 },
            uIorB: { value: 1.22 },
            uIorP: { value: 1.22 },
            uRefractPower: { value: 0.33 },
            uChromaticAberration: { value: 2.0 },
            uSaturation: { value: 1.08 },
            uShininess: { value: 40.0 },
            uDiffuseness: { value: 0.2 },
            uFresnelPower: { value: 8.0 },
            uLight: { value: new THREE.Vector3(2, 0, 1) },
            winResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
        }
    });

    const fontLoader = new THREE.FontLoader();
    const font = await new Promise((resolve) => {
        fontLoader.load('/static/fonts/Montserrat Black_Regular.json', resolve);
    });

    const textGeometry = new THREE.TextGeometry('MAKE\nYOUR\nMARK', {
        font: font,
        size: 0.8,
        height: 0,
    });
    const textMaterial = new THREE.MeshStandardMaterial({ color: 'white' });
    const textMesh = new THREE.Mesh(textGeometry, textMaterial);
    textMesh.position.set(0, 1.0, 0); 
    scene.add(textMesh)

    // torus mesh
    const torusGeometry = new THREE.TorusGeometry(0.6, 0.25, 12, 48);
    const torusMesh = new THREE.Mesh(torusGeometry, shaderMaterial);
    torusMesh.position.set(0, 0.5, 0.5);
    scene.add(torusMesh);

    // icosahedron mesh
    const icosahedronGeometry = new THREE.IcosahedronGeometry( 0.22, 5);
    const icosahedronMesh = new THREE.Mesh(icosahedronGeometry, shaderMaterial);
    icosahedronMesh.position.set(0.1, -0.7, 2.8);
    scene.add(icosahedronMesh);

    // cylinder mesh
    const cylinderGeometry = new THREE.CylinderGeometry( 0.1, 0.1, 1, 32);
    const cylinderMesh = new THREE.Mesh(cylinderGeometry, shaderMaterial);
    cylinderMesh.position.set(0.5, -0.1, 3.0);
    scene.add(cylinderMesh);

    // light
    const light = new THREE.AmbientLight( 0xffffff, 1 )
    scene.add(light)

    const clock = new THREE.Clock();
    function animate() {
        const elapsedTime = clock.getElapsedTime();
        requestAnimationFrame(animate);

        renderer.setRenderTarget(backRenderTarget);
        renderer.render(scene, camera);

        shaderMaterial.uniforms.uTexture.value = backRenderTarget.texture;
        shaderMaterial.side = THREE.BackSide;

        renderer.setRenderTarget(mainRenderTarget);
        renderer.render(scene, camera);

        shaderMaterial.uniforms.uTexture.value = mainRenderTarget.texture;
        shaderMaterial.side = THREE.FrontSide;

        torusMesh.position.y = Math.sin(elapsedTime * 0.1 * 0.5) * 0.5;
        torusMesh.rotation.x += 0.001;
        torusMesh.rotation.y += 0.001;

        icosahedronMesh.position.y = Math.sin(elapsedTime * 0.1 * 0.5 + (Math.PI / 2)) * 0.5;
   
        cylinderMesh.position.y = Math.sin(elapsedTime * 0.1 * 0.5 + Math.PI) * 0.5;
        cylinderMesh.rotation.x += 0.001;
        cylinderMesh.rotation.y += 0.001;

        renderer.setRenderTarget(null);
        renderer.render(scene, camera);
    }

    animate();

    window.addEventListener('resize', () => {
        const width = window.innerWidth;
        const height = window.innerHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        mainRenderTarget.setSize(width, height);
        backRenderTarget.setSize(width, height);
        shaderMaterial.uniforms.winResolution.value.set(width, height).multiplyScalar(Math.min(window.devicePixelRatio, 2));
    });
})();
