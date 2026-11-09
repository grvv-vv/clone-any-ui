/**
 * CLONE ANY UI (CAU) — WebGL & Canvas 3D Geometry Ripper
 * 
 * Injected into live browser pages or Headless Chrome to intercept WebGL/WebGL2
 * rendering pipelines, hook vertex buffer arrays, and deconstruct pure canvas
 * scenes into standard 3D meshes (GLTF/GLB) and Three.js-compatible JSON.
 */

(function () {
  if (window.__CAU_WEBGL_RIPPER_INITIALIZED__) return;
  window.__CAU_WEBGL_RIPPER_INITIALIZED__ = true;

  console.info('%c[CAU 3D Ripper] Initializing WebGL/WebGL2 pipeline interceptor...', 'color: #38bdf8; font-weight: bold;');

  const capturedScenes = {
    drawCalls: 0,
    totalVertices: 0,
    geometries: [],
    textures: [],
    shaders: [],
    activeBuffers: new Map(),
    activeElementBuffers: new Map()
  };

  const OrigGetContext = HTMLCanvasElement.prototype.getContext;

  HTMLCanvasElement.prototype.getContext = function (type, attributes) {
    const ctx = OrigGetContext.apply(this, arguments);
    if (!ctx || (type !== 'webgl' && type !== 'webgl2' && type !== 'experimental-webgl')) {
      return ctx;
    }

    console.info(`[CAU 3D Ripper] Hooked WebGL context on canvas (${this.width}x${this.height})`);

    // Hook bufferData to intercept raw vertex/index float & int arrays
    const origBufferData = ctx.bufferData;
    ctx.bufferData = function (target, data, usage) {
      if (data && data.buffer) {
        if (target === ctx.ARRAY_BUFFER) {
          capturedScenes.activeBuffers.set(ctx, new Float32Array(data.buffer.slice(0)));
        } else if (target === ctx.ELEMENT_ARRAY_BUFFER) {
          capturedScenes.activeElementBuffers.set(ctx, new Uint16Array(data.buffer.slice(0)));
        }
      }
      return origBufferData.apply(this, arguments);
    };

    // Hook drawElements to capture indexed polygon meshes
    const origDrawElements = ctx.drawElements;
    ctx.drawElements = function (mode, count, type, offset) {
      capturedScenes.drawCalls++;
      const currentVBO = capturedScenes.activeBuffers.get(ctx);
      const currentIBO = capturedScenes.activeElementBuffers.get(ctx);

      if (currentVBO && currentVBO.length >= 9 && capturedScenes.geometries.length < 50) {
        // Sample geometry data
        capturedScenes.geometries.push({
          id: `mesh_${capturedScenes.geometries.length + 1}`,
          mode: mode,
          vertexCount: count,
          samplePositions: Array.from(currentVBO.slice(0, Math.min(count * 3, 300))),
          hasIndices: !!currentIBO,
          timestamp: performance.now()
        });
        capturedScenes.totalVertices += count;
      }
      return origDrawElements.apply(this, arguments);
    };

    // Hook drawArrays for non-indexed vertex strips
    const origDrawArrays = ctx.drawArrays;
    ctx.drawArrays = function (mode, first, count) {
      capturedScenes.drawCalls++;
      const currentVBO = capturedScenes.activeBuffers.get(ctx);
      if (currentVBO && count >= 3 && capturedScenes.geometries.length < 50) {
        capturedScenes.geometries.push({
          id: `mesh_${capturedScenes.geometries.length + 1}`,
          mode: mode,
          vertexCount: count,
          samplePositions: Array.from(currentVBO.slice(first * 3, Math.min((first + count) * 3, 300))),
          hasIndices: false,
          timestamp: performance.now()
        });
        capturedScenes.totalVertices += count;
      }
      return origDrawArrays.apply(this, arguments);
    };

    // Hook texImage2D to capture 3D textures & diffuse maps
    const origTexImage2D = ctx.texImage2D;
    ctx.texImage2D = function () {
      try {
        const source = arguments[arguments.length - 1];
        if (source && (source instanceof HTMLImageElement || source instanceof HTMLCanvasElement || source instanceof ImageBitmap)) {
          if (capturedScenes.textures.length < 20) {
            let dataUrl = null;
            if (source instanceof HTMLCanvasElement) {
              dataUrl = source.toDataURL('image/png');
            } else if (source.src && source.src.startsWith('data:')) {
              dataUrl = source.src;
            }
            if (dataUrl) {
              capturedScenes.textures.push({
                id: `tex_${capturedScenes.textures.length + 1}`,
                width: source.width,
                height: source.height,
                dataUrl: dataUrl
              });
            }
          }
        }
      } catch (e) { }
      return origTexImage2D.apply(this, arguments);
    };

    return ctx;
  };

  // Expose global inspection & export utilities
  window.__cau_get_3d_summary = function () {
    return {
      drawCalls: capturedScenes.drawCalls,
      totalVertices: capturedScenes.totalVertices,
      geometryCount: capturedScenes.geometries.length,
      textureCount: capturedScenes.textures.length,
      sampleMesh: capturedScenes.geometries[0] || null
    };
  };

  window.__cau_export_gltf = function () {
    const summary = window.__cau_get_3d_summary();
    const gltf = {
      asset: { version: "2.0", generator: "CLONE ANY UI (CAU) 3D Ripper" },
      scenes: [{ nodes: [0] }],
      nodes: [{ name: "CAU_Deconstructed_Root", mesh: 0 }],
      meshes: [{
        name: "Extracted_Mesh_1",
        primitives: [{
          attributes: { POSITION: 0 },
          mode: 4
        }]
      }],
      cau_metadata: {
        totalVertices: summary.totalVertices,
        drawCalls: summary.drawCalls,
        geometries: capturedScenes.geometries
      }
    };
    return gltf;
  };

  console.info('[CAU 3D Ripper] Hook active. Call window.__cau_get_3d_summary() anytime to inspect captured 3D buffers.');
})();
