/* eslint-disable no-confusing-arrow */
import { useEffect, useRef, useState } from 'react';
import { Box, Typography, Flex, IconButton, LoadingSpinner, Drawer } from '@neo4j-ndl/react';
import { ClockIconOutline } from '@neo4j-ndl/react/icons';
import './Retrieval.css';
import retrievalIllustration from '../assets/retrieval.png';

import { setDriver, runQuery } from '../utils/Driver';

import { ResetZoomIcon, FitToScreenIcon } from '@neo4j-ndl/react/icons';

import type NVL from '@neo4j-nvl/base';

import type { HitTargets, Node, Relationship } from '@neo4j-nvl/base';
import { InteractiveNvlWrapper } from '@neo4j-nvl/react';
import type { MouseEventCallbacks } from '@neo4j-nvl/react';
import ReactMarkdown from 'react-markdown';

type CypherProps = {
  uri?: string;
  username?: string;
  password?: string;
};

function RetrievalInformation({ sources, model, entities, timeTaken }) {

  const nvl = useRef<NVL | null>(null);
  const [uri, setURI] = useState(import.meta.env.VITE_NEO4J_URI);
  const [username, setUsername] = useState(import.meta.env.VITE_NEO4J_USERNAME);
  const [password, setPassword] = useState(import.meta.env.VITE_NEO4J_PASSWORD);
  const [loading, setLoading] = useState(true);
  const [isExpanded, handleIsExpanded] = useState(false);
  const [expandedNode, setExpandedNode] = useState(null);

  const handleExpand = (nodes, hitTargets, evt) => {
    setExpandedNode(nodes);
    handleIsExpanded(true);
  }

  useEffect(() => {
    run();
  
  }, []);

  const [nodes, setNodes] = useState<Node[]>([]);
  const [rels, setRels] = useState<Relationship[]>([]);

  const fitNodes = () => {
    nvl.current?.fit(nodes.map((n) => n.id));
  };
  const resetZoom = () => {
    nvl.current?.resetZoom();
  };

  const mouseEventCallbacks: MouseEventCallbacks = {
    onHover: (element: Node | Relationship, hitTargets: HitTargets, evt: MouseEvent) =>
      console.log('onHover', element, hitTargets, evt),
    onRelationshipRightClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) =>
      console.log('onRelationshipRightClick', rel, hitTargets, evt),
    onNodeClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) =>
      handleExpand(node, hitTargets, evt),
    onNodeRightClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) =>
      console.log('onNodeRightClick', node, hitTargets, evt),
    onNodeDoubleClick: (node: Node, hitTargets: HitTargets, evt: MouseEvent) =>
      console.log('onNodeDoubleClick', node, hitTargets, evt),
    onRelationshipClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) =>
      console.log('onRelationshipClick', rel, hitTargets, evt),
    onRelationshipDoubleClick: (rel: Relationship, hitTargets: HitTargets, evt: MouseEvent) =>
      console.log('onRelationshipDoubleClick', rel, hitTargets, evt),
    onCanvasClick: (evt: MouseEvent) => console.log('onCanvasClick', evt),
    onCanvasDoubleClick: (evt: MouseEvent) => console.log('onCanvasDoubleClick', evt),
    onCanvasRightClick: (evt: MouseEvent) => console.log('onCanvasRightClick', evt),
    onDrag: (nodes: Node[]) => console.log('onDrag', nodes),
    onPan: (evt: MouseEvent) => console.log('onPan', evt),
    onZoom: (zoomLevel: number) => console.log('onZoom', zoomLevel),
  };

  function run() {
    const formattedSources = sources.map((source) => `"${source}"`).join(',');
    const query2 = `  
    MATCH (a:Chunk)-[r2:PART_OF]-(d:Document) WHERE elementId(a) in [${formattedSources}]
    MATCH (a)-[r]-(b:__Entity__)
    WHERE elementId(b) IN [${formattedSources}]
    RETURN a, r, b, r2, d LIMIT 100

    `;
    setDriver(uri, username, password).then((isSuccessful) => {
      runQuery(query2).then((result) => {
        result.nodes.map((record: any) => {
          const label = record.labels.includes("__Entity__") ? record.properties.id : record.labels;
          const color = record.labels.includes('Chunk')
            ? '#0A6190'
            : record.labels.includes('Document')
            ? '#BCF194'
            : record.labels.includes('__Entity__')
            ? '#B38EFF'
            : '#FF8E6A';
          setNodes((prevNodes) => [
            ...prevNodes,
            { id: record.id.toString(), color: color, captions: [{ value: label }], properties: record.properties },
          ]);
        });

        result.rels.map((record: any) => {
          setRels((prevRels) => [
            ...prevRels,
            {
              id: record.id.toString(),
              from: record.start.toString(),
              to: record.end.toString(),
              captions: [{ value: record.type.toString() }],
            },
          ]);
        });
        setLoading(false);
      });
    });
  }

  return (
    <Box className='n-bg-palette-neutral-bg-weak p-4'>
      <Flex flexDirection='row' className='flex flex-row p-6 items-center'>
        <img src={retrievalIllustration} alt='icon' style={{ width: 95, height: 95, marginRight: 10 }} />
        <Box className='flex flex-col'>
          <Typography variant='h2'>Retrieval information</Typography>
          <Typography className='mb-2' variant='body-medium'>
            To generate this response, we used the model <span className='font-bold italic'>{model}</span>.
            <Typography className='pl-1 italic' variant='body-small'>
              <ClockIconOutline className='w-4 h-4 inline-block mb-1' /> {timeTaken / 1000} seconds
            </Typography>
          </Typography>
        </Box>
      </Flex>
      <Box className='button-container' sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
        <div
          style={{
            margin: 10,
            borderRadius: 25,
            border: '2px solid #2AADA5',
            height: 650,
            background: `rgb(var(--theme-palette-primary-bg-weaker));`,
            boxShadow: `2px -2px 10px grey`,
            position: 'relative',
          }}
        >
          <Flex
            flexDirection='row'
            className='flex flex-row p-6'
            style={{
              position: 'absolute',
              top: 0,
              right: 0,
              zIndex: 1000,
            }}
          >
            <IconButton className='n-size-token-7' ariaLabel='Fit to screen' onClick={fitNodes}>
              <FitToScreenIcon />
            </IconButton>
            <IconButton className='n-size-token-7' ariaLabel='Reset zoom' onClick={resetZoom}>
              <ResetZoomIcon />
            </IconButton>
          </Flex>
          {loading ? (
            <LoadingSpinner
              size='large'
              style={{
                position: 'absolute',
                top: '50%',
                right: '50%',
              }}
            />
          ) : (
            <></>
          )}
          <InteractiveNvlWrapper
            ref={nvl}
            nodes={nodes}
            rels={rels}
            onClick={(evt) => console.log('custom click event', evt)}
            mouseEventCallbacks={mouseEventCallbacks}
            nvlOptions={{
              initialZoom: 0,
              layout: 'd3Force',
              relationshipThreshold: 1,
            }}
          />
          <Box className='max-w-[300px]'>
            <Drawer isCloseable={true} isExpanded={isExpanded} position="left" type="overlay" onExpandedChange={() => {
              handleIsExpanded(false);
            }}>
              <Drawer.Header>Node details</Drawer.Header>
              <Drawer.Body className='max-w-[300px]'>
                {expandedNode?.captions[0]?.value?.includes('Chunk') ? (<Typography variant='h5'>Chunk text: </Typography>) : expandedNode?.captions[0]?.value?.includes('Document') ? (<Typography variant='h5'>Document: </Typography>) : (<Typography variant='h5'>Entity description: </Typography>)}
                <ReactMarkdown>
                  {expandedNode?.properties?.text ?? expandedNode?.properties?.fileName ?? expandedNode?.properties?.id}
                </ReactMarkdown>
                </Drawer.Body>
            </Drawer>
          </Box>
        </div>
      </Box>
    </Box>
  );
}

export default RetrievalInformation;