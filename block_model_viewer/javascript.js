$(document).ready(function() {
    if (WEBGL.isWebGLAvailable() === false) {
        document.body.appendChild( WEBGL.getWebGLErrorMessage() );
    }

    var camera, scene, renderer;
    var controls;
    var cubeGeometry;
    var blockMeshes = [];
    var dataMap;
    var blocks;
    var blockSize = 50;
    var currentGrade = "Au";
    var transparent = false;

    init();
    animate();

    function init() {
        createScene();
        createLights();
        createObjects();
        createCamera();
        createRenderer();
        createCameraControls();
        setEventListeners();
    }
    
    function createScene() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color( 0xf0f0f0 );
    }
    
    function createLights() {
        var ambientLight = new THREE.AmbientLight( 0x606060 );
        scene.add( ambientLight );
    
        var light = new THREE.PointLight( 0xffffff );
        light.position.set( 1000, 1000, 1000 );
        scene.add( light );
    }
    
    function createObjects() {
        function fetchDataMap(idBlockModel) {
            var url = encodeURI("http://127.0.0.1:8000/block_models/"+idBlockModel+"/data_map");	
            fetch(url)
                .then(function(response) {
                    var data = response.json();
                    var promise = Promise.resolve(data);
                    promise.then(function(value) {
                        dataMap = value.data_map
                        fetchBlocks(idBlockModel);
                    });
                });
        }
    
        function fetchBlocks(idBlockModel) {
            var url = encodeURI("http://127.0.0.1:8000/block_models/"+idBlockModel+"/blocks/");	
            fetch(url)
                .then(function(response) {
                    var data = response.json();
                    var promise = Promise.resolve(data);
                    promise.then(function(value) {
                        blocks = value.blocks
                        loadBlockModel();
                    });
                });
        }
    
        cubeGeometry = new THREE.BoxBufferGeometry( blockSize, blockSize, blockSize );
        var idBlockModel = "5ceb2e1f107fae448cf06f5a";
        fetchDataMap(idBlockModel);
    }
    
    function loadBlockModel() {
        var gradeHeader = dataMap.grade[currentGrade];
        var xIndex = dataMap["x"];
        var yIndex = dataMap["y"];
        var zIndex = dataMap["z"];
        function addBlock(block) {
            var cubeMaterial = new THREE.MeshLambertMaterial({
                color: getBlockColor(block), 
                opacity: Math.max(0.01, block[gradeHeader]),
                transparent: transparent 
            });
            var blockMesh = new THREE.Mesh(cubeGeometry, cubeMaterial);
            
            var blockSizeWithOffset = blockSize * 1.1;
            blockMesh.position.set(
                blockSizeWithOffset * block[xIndex],
                blockSizeWithOffset * block[yIndex],
                 blockSizeWithOffset * block[zIndex]
            );
            blockMeshes.push(blockMesh);
            scene.add( blockMesh );        
        }
    
        function getBlockColor(block) {
            if (block[gradeHeader] < 0.001)
                return new THREE.Color(0x999999);
            var hue = currentGrade == "Cu" ? 168 : 50;
            var lightning = Math.floor(block[gradeHeader] * 70);
            var hsl = "hsl("+ hue + ", 100%, " + lightning + "%)";
            return new THREE.Color(hsl);
        }
    
        clearScene();
        for(var i=0; i<blocks.length; i++) {
            addBlock(blocks[i]);
        }
    }
    
    function createCamera() {
        camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
        camera.position.set( 2000, 2000, 3300 );
        camera.lookAt( 0, 0, 0 );
        camera.up.set(0, 0, 1);
        scene.add(camera);
    }
    
    function createRenderer() {
        renderer = new THREE.WebGLRenderer( { antialias: true } );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.setSize( window.innerWidth, window.innerHeight );
        document.body.appendChild( renderer.domElement );
    }
    
    function createCameraControls() {
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.update();
    }
    
    function setEventListeners() {
        window.addEventListener( 'resize', onWindowResize, false );
        document.addEventListener( 'keydown', onDocumentKeyDown, false );
    }
    
    function clearScene() {
        for(var i=0; i<blockMeshes.length; i++) {
            scene.remove(blockMeshes[i]);
        }; 
    }
    
    function onWindowResize() {
    
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    
        renderer.setSize( window.innerWidth, window.innerHeight );
    
    }
    
    function onDocumentKeyDown( event ) {
        switch ( event.keyCode ) {
            case 65: //a
                currentGrade = "Au";
                loadBlockModel();
                break;
            case 67: //c
                currentGrade = "Cu";
                loadBlockModel();
                break;
            case 84: //t
                transparent = !transparent;
                loadBlockModel();
                break;
    
        }
    }
    
    function animate() {
    
        requestAnimationFrame( animate );
    
        controls.update();
    
        renderer.render( scene, camera );
    
    }
})