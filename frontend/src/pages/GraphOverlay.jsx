// GraphPopup.jsx
import React, { useEffect } from "react";
import ReactFlow, { useNodesState, useEdgesState, MarkerType } from "react-flow-renderer";
import "./GraphOverlay.css";

export default function GraphPopup({ activeNodeId }) {
  const initialNodes = [
    { id: "manager_agent", position: { x: 400, y: 200 }, data: { label: "Manager Agent" }, style: { color: "white" } },
    { id: "data_overview", position: { x: 400, y: 50 }, data: { label: "Data Overview" }, style: { color: "white" } },
    { id: "planning_agent", position: { x: 300, y: 300 }, data: { label: "Planning Agent" }, style: { color: "white" } },
    { id: "chart_drawing_agent", position: { x: 500, y: 300 }, data: { label: "Chart Drawing" }, style: { color: "white" } },
    { id: "chart_analysis_agent", position: { x: 700, y: 300 }, data: { label: "Chart Analysis" }, style: { color: "white" } },
    { id: "insights_agent", position: { x: 900, y: 300 }, data: { label: "Insights Agent" }, style: { color: "white" } },
    { id: "END", position: { x: 400, y: 500 }, data: { label: "END" }, style: { color: "white" } },
  ];

  const initialEdges = [
    { id: "e0-1", source: "data_overview", target: "manager_agent", animated: true, markerEnd: { type: MarkerType.Arrow } },
    { id: "e1-2", source: "manager_agent", target: "planning_agent", animated: true, markerEnd: { type: MarkerType.Arrow } },
    { id: "e2-3", source: "manager_agent", target: "chart_drawing_agent", animated: true, markerEnd: { type: MarkerType.Arrow } },
    { id: "e2-4", source: "manager_agent", target: "chart_analysis_agent", animated: true, markerEnd: { type: MarkerType.Arrow } },
    { id: "e2-5", source: "manager_agent", target: "insights_agent", animated: true, markerEnd: { type: MarkerType.Arrow } },
    { id: "e2-6", source: "manager_agent", target: "END", animated: true, markerEnd: { type: MarkerType.Arrow } },
  ];

  const [nodes, setNodes] = useNodesState(initialNodes);
  const [edges] = useEdgesState(initialEdges);

  useEffect(() => {
    setNodes(nds =>
      nds.map(node => ({
        ...node,
        style: {
          ...node.style,
          border: node.id === activeNodeId ? "3px solid #14f1ff" : "1px solid #888",
          background: node.id === activeNodeId ? "#0e1e26" : "#1a1a1a",
          transition: "0.25s",
        },
      }))
    );
  }, [activeNodeId]);

  return (
    <div className="mini-graph-container">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        panOnDrag={false}
        zoomOnScroll={false}
        zoomOnPinch={false}
        zoomOnDoubleClick={false}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
      />
    </div>
  );
}
