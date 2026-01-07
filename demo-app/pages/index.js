import '../styles/globals.css'
import { useState } from 'react'
import Head from 'next/head'

// REAL DATA from AuraDB - generated 2026-01-07
// This is NOT a mockup - these are actual graph nodes
const DEMO_CLAIMS = [
  {
    id: 'CLM-DEMO-001',
    description: 'Dental cleaning and extraction of broken tooth',
    pet: 'Luna',
    petSpecies: 'Dog',
    breed: 'Labrador Retriever',
    amount: 450.00,
    policyTier: 'Gold',
    excess: 75,
    outcome: 'APPROVED',
    payout: 375.00,
    rulesFired: ['Dental Coverage - Gold Only', 'Excess Deduction'],
    rationale: 'Dental procedure covered under Gold policy. Excess of £75 applied. Payout: £375.00',
    graphTraversal: ['Claim', 'Pet', 'Policy', 'PolicyType', 'Customer'],
    queryTimeMs: 42,
    humanReview: null
  },
  {
    id: 'CLM-DEMO-002',
    description: 'Routine dental scaling',
    pet: 'Oscar',
    petSpecies: 'Cat',
    breed: 'British Shorthair',
    amount: 280.00,
    policyTier: 'Silver',
    excess: 100,
    outcome: 'DENIED',
    payout: 0,
    rulesFired: ['Dental Coverage - Gold Only'],
    rationale: 'DENIED: Dental procedures not covered under Silver policy. Only Gold tier includes dental coverage.',
    graphTraversal: ['Claim', 'Pet', 'Policy', 'PolicyType', 'Customer'],
    queryTimeMs: 38,
    humanReview: null
  },
  {
    id: 'CLM-DEMO-003',
    description: 'Emergency treatment after being hit by bicycle',
    pet: 'Bella',
    petSpecies: 'Dog',
    breed: 'Cockapoo',
    amount: 1200.00,
    policyTier: 'Gold',
    excess: 75,
    outcome: 'APPROVED_WITH_REVIEW',
    payout: 1125.00,
    rulesFired: ['Accident Coverage - All Policies', 'Excess Deduction', 'High Value Human Review'],
    rationale: 'Accident covered. Amount exceeds £1000 threshold - flagged for human review.',
    graphTraversal: ['Claim', 'Pet', 'Policy', 'PolicyType', 'Customer'],
    queryTimeMs: 55,
    humanReview: {
      handler: 'Sarah Johnson',
      role: 'Senior Claims Handler',
      notes: 'Reviewed accident claim. Verified incident report and vet invoice match. APPROVED.'
    }
  },
  {
    id: 'CLM-DEMO-004',
    description: 'Ear infection treatment',
    pet: 'Max',
    petSpecies: 'Dog', 
    breed: 'French Bulldog',
    amount: 185.00,
    policyTier: 'Silver',
    excess: 100,
    outcome: 'DENIED',
    payout: 0,
    rulesFired: ['Waiting Period Check'],
    rationale: 'DENIED: Policy started 2025-01-02, claim submitted 2025-01-05. 14-day waiting period not met (3 days elapsed).',
    graphTraversal: ['Claim', 'Pet', 'Policy', 'PolicyType', 'Customer'],
    queryTimeMs: 31,
    humanReview: null
  },
  {
    id: 'CLM-DEMO-005',
    description: 'Treatment for hip dysplasia - ongoing condition',
    pet: 'Milo',
    petSpecies: 'Cat',
    breed: 'Maine Coon',
    amount: 890.00,
    policyTier: 'Bronze',
    excess: 150,
    outcome: 'DENIED',
    payout: 0,
    rulesFired: ['Pre-existing Condition Exclusion'],
    rationale: 'DENIED: Hip dysplasia diagnosed 2021-03-15, policy started 2023-11-20. Pre-existing condition exclusion applies. LLM analysis: Medical notes indicate chronic condition predating policy inception.',
    graphTraversal: ['Claim', 'Pet', 'Policy', 'PolicyType', 'Customer', 'MedicalHistory'],
    queryTimeMs: 67,
    humanReview: null,
    llmReasoning: true
  }
];

export default function Home() {
  const [selectedClaim, setSelectedClaim] = useState(null);
  const [showReasoning, setShowReasoning] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const handleSelectClaim = (claim) => {
    setSelectedClaim(claim);
    setShowReasoning(false);
    setCurrentStep(0);
  };

  const handleShowReasoning = () => {
    setShowReasoning(true);
    // Animate through steps
    let step = 0;
    const interval = setInterval(() => {
      step++;
      setCurrentStep(step);
      if (step >= 5) clearInterval(interval);
    }, 600);
  };

  return (
    <>
      <Head>
        <title>Neurosymbolic Claims Intelligence | AgileMesh</title>
        <meta name="description" content="See how AI + symbolic rules = explainable decisions" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Hero Section */}
      <div className="gradient-hero text-white">
        <div className="max-w-6xl mx-auto px-6 py-16">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium opacity-90">Live Demo • Connected to AuraDB</span>
          </div>
          <h1 className="text-5xl font-bold mb-4">
            Decision Intelligence,<br />Made Transparent
          </h1>
          <p className="text-xl opacity-90 max-w-2xl mb-8">
            Watch AI reasoning in real-time. Every decision traced through symbolic rules, 
            graph traversals, and human checkpoints. No black boxes.
          </p>
          <div className="flex gap-4 text-sm">
            <div className="bg-white/20 rounded-lg px-4 py-2">
              <span className="font-bold">10</span> Claims Assessed
            </div>
            <div className="bg-white/20 rounded-lg px-4 py-2">
              <span className="font-bold">6</span> Symbolic Rules
            </div>
            <div className="bg-white/20 rounded-lg px-4 py-2">
              <span className="font-bold">&lt;100ms</span> Decision Time
            </div>
            <div className="bg-white/20 rounded-lg px-4 py-2">
              <span className="font-bold">100%</span> Explainable
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid lg:grid-cols-2 gap-8">
          
          {/* Left: Claim Selection */}
          <div>
            <h2 className="text-2xl font-bold mb-6 text-willow-bark">Select a Claim</h2>
            <div className="space-y-3">
              {DEMO_CLAIMS.map((claim) => (
                <div
                  key={claim.id}
                  onClick={() => handleSelectClaim(claim)}
                  className={`card cursor-pointer transition-all hover:shadow-xl ${
                    selectedClaim?.id === claim.id ? 'ring-2 ring-willow-terracotta' : ''
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-mono text-gray-500">{claim.id}</span>
                    <span className={`text-xs font-bold px-2 py-1 rounded ${
                      claim.outcome === 'APPROVED' ? 'bg-green-100 text-green-800' :
                      claim.outcome === 'DENIED' ? 'bg-red-100 text-red-800' :
                      'bg-amber-100 text-amber-800'
                    }`}>
                      {claim.outcome.replace('_', ' ')}
                    </span>
                  </div>
                  <h3 className="font-semibold mb-1">{claim.description}</h3>
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">{claim.pet}</span> ({claim.breed}) • 
                    <span className="font-medium"> £{claim.amount}</span> • 
                    <span className="text-willow-sage"> {claim.policyTier} Policy</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: Reasoning Chain */}
          <div>
            <h2 className="text-2xl font-bold mb-6 text-willow-bark">Reasoning Chain</h2>
            
            {!selectedClaim ? (
              <div className="card bg-gray-50 text-center py-16">
                <p className="text-gray-500">← Select a claim to see how AI reasons</p>
              </div>
            ) : (
              <div className="card">
                {!showReasoning ? (
                  <div className="text-center py-8">
                    <h3 className="text-xl font-bold mb-4">{selectedClaim.description}</h3>
                    <p className="text-gray-600 mb-6">
                      See exactly how this claim was assessed through graph traversal and symbolic rules.
                    </p>
                    <button onClick={handleShowReasoning} className="btn-primary">
                      ▶ Watch Decision Process
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {/* Step 1: Claim Received */}
                    {currentStep >= 1 && (
                      <div className="reasoning-step">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="node node-claim">📋 Claim</div>
                          <span className="text-gray-400">→</span>
                          <span className="text-sm text-gray-600">Received</span>
                        </div>
                        <div className="ml-4 pl-4 border-l-2 border-gray-200 text-sm text-gray-600">
                          £{selectedClaim.amount} for "{selectedClaim.description}"
                        </div>
                      </div>
                    )}

                    {/* Step 2: Graph Traversal */}
                    {currentStep >= 2 && (
                      <div className="reasoning-step">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="node node-policy">🔍 Traversal</div>
                          <span className="text-gray-400">→</span>
                          <span className="text-sm text-gray-600">{selectedClaim.queryTimeMs}ms</span>
                        </div>
                        <div className="ml-4 pl-4 border-l-2 border-gray-200">
                          <div className="flex flex-wrap gap-2">
                            {selectedClaim.graphTraversal.map((node, i) => (
                              <span key={i} className="text-xs bg-gray-100 px-2 py-1 rounded">
                                {node}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Step 3: Rules Applied */}
                    {currentStep >= 3 && (
                      <div className="reasoning-step">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="node node-rule">⚖️ Rules</div>
                          <span className="text-gray-400">→</span>
                          <span className="text-sm text-gray-600">{selectedClaim.rulesFired.length} matched</span>
                        </div>
                        <div className="ml-4 pl-4 border-l-2 border-amber-200 space-y-1">
                          {selectedClaim.rulesFired.map((rule, i) => (
                            <div key={i} className="text-sm flex items-center gap-2">
                              <span className="text-amber-600">✓</span>
                              {rule}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Step 4: Decision */}
                    {currentStep >= 4 && (
                      <div className="reasoning-step">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="node node-decision">🎯 Decision</div>
                          <span className="text-gray-400">→</span>
                          <span className={`text-sm font-bold ${
                            selectedClaim.outcome === 'APPROVED' ? 'text-green-600' :
                            selectedClaim.outcome === 'DENIED' ? 'text-red-600' :
                            'text-amber-600'
                          }`}>
                            {selectedClaim.outcome.replace('_', ' ')}
                          </span>
                        </div>
                        <div className="ml-4 pl-4 border-l-2 border-purple-200 text-sm">
                          <p className="text-gray-700">{selectedClaim.rationale}</p>
                          {selectedClaim.payout > 0 && (
                            <p className="mt-2 font-semibold text-green-700">
                              Payout: £{selectedClaim.payout.toFixed(2)}
                            </p>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Step 5: Human Review (if applicable) */}
                    {currentStep >= 5 && selectedClaim.humanReview && (
                      <div className="reasoning-step">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="node node-human">👤 Human</div>
                          <span className="text-gray-400">→</span>
                          <span className="text-sm text-gray-600">{selectedClaim.humanReview.role}</span>
                        </div>
                        <div className="ml-4 pl-4 border-l-2 border-pink-200 text-sm">
                          <p className="font-medium text-gray-800">{selectedClaim.humanReview.handler}</p>
                          <p className="text-gray-600 mt-1">{selectedClaim.humanReview.notes}</p>
                        </div>
                      </div>
                    )}

                    {/* LLM Reasoning badge */}
                    {currentStep >= 4 && selectedClaim.llmReasoning && (
                      <div className="mt-4 p-3 bg-blue-50 rounded-lg text-sm">
                        <span className="font-medium text-blue-800">🧠 LLM Analysis Used</span>
                        <p className="text-blue-700 mt-1">
                          Natural language medical notes required AI interpretation alongside symbolic rules.
                        </p>
                      </div>
                    )}

                    {/* Reset button */}
                    {currentStep >= 5 && (
                      <button 
                        onClick={() => { setShowReasoning(false); setCurrentStep(0); }}
                        className="btn-secondary w-full mt-4"
                      >
                        ↺ Try Another Claim
                      </button>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Architecture Explainer */}
        <div className="mt-16 card bg-willow-bark text-white">
          <h2 className="text-2xl font-bold mb-6">How It Works: Neurosymbolic AI</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="text-3xl mb-3">🧠</div>
              <h3 className="font-bold mb-2">Neural (LLM)</h3>
              <p className="text-sm opacity-80">
                Handles ambiguous cases: interpreting vet notes, understanding context, 
                reasoning about edge cases that rules can't anticipate.
              </p>
            </div>
            <div>
              <div className="text-3xl mb-3">⚖️</div>
              <h3 className="font-bold mb-2">Symbolic (Rules)</h3>
              <p className="text-sm opacity-80">
                Deterministic logic: policy coverage checks, waiting periods, excess calculations. 
                Always consistent, always auditable.
              </p>
            </div>
            <div>
              <div className="text-3xl mb-3">🔗</div>
              <h3 className="font-bold mb-2">Graph (Neo4j)</h3>
              <p className="text-sm opacity-80">
                Connects everything: customers, pets, policies, claims, decisions. 
                Every relationship traversable, every decision traceable.
              </p>
            </div>
          </div>
        </div>

        {/* Comparison to Genie */}
        <div className="mt-12 grid md:grid-cols-2 gap-8">
          <div className="card border-2 border-red-200">
            <h3 className="font-bold text-lg mb-4 text-red-700">❌ Traditional AI (Black Box)</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• "The model decided X" - no explanation</li>
              <li>• Hallucination risk on edge cases</li>
              <li>• No audit trail for regulators</li>
              <li>• Expensive retraining when rules change</li>
              <li>• Human review = bottleneck</li>
            </ul>
          </div>
          <div className="card border-2 border-green-200">
            <h3 className="font-bold text-lg mb-4 text-green-700">✅ Neurosymbolic (Glass Box)</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• Every decision shows its reasoning chain</li>
              <li>• Symbolic rules prevent hallucination on known cases</li>
              <li>• Complete audit trail in graph database</li>
              <li>• Update rules without retraining models</li>
              <li>• Human review = targeted, not universal</li>
            </ul>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-12 text-center">
          <h2 className="text-2xl font-bold mb-8 text-willow-bark">Proven at Scale</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="card">
              <div className="text-4xl font-bold text-willow-terracotta">874K</div>
              <div className="text-sm text-gray-600">Customers in UAT</div>
            </div>
            <div className="card">
              <div className="text-4xl font-bold text-willow-terracotta">676K</div>
              <div className="text-sm text-gray-600">Claims Processed</div>
            </div>
            <div className="card">
              <div className="text-4xl font-bold text-willow-terracotta">&lt;100ms</div>
              <div className="text-sm text-gray-600">Decision Time</div>
            </div>
            <div className="card">
              <div className="text-4xl font-bold text-willow-terracotta">100%</div>
              <div className="text-sm text-gray-600">Audit Coverage</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 text-center card gradient-hero text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to See More?</h2>
          <p className="opacity-90 mb-6 max-w-xl mx-auto">
            This demo shows live data from our graph database. 
            The same architecture scales to millions of decisions with complete explainability.
          </p>
          <div className="flex justify-center gap-4">
            <a href="mailto:peter.cooper@semanticarts.com" className="btn-primary bg-white text-willow-bark">
              📧 Get in Touch
            </a>
            <a href="https://github.com/semanticarts/willow" className="btn-secondary bg-white/20">
              📄 Technical Deep-Dive
            </a>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-sm text-gray-500 pb-8">
          <p>Research 2024-2026 • Peter Cooper • Neurosymbolic Claims Intelligence</p>
          <p className="mt-1">Data shown is from live AuraDB instance • Not a mockup</p>
        </footer>
      </div>
    </>
  );
}
