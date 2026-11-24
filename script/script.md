# THE MACHINE THAT BORROWS THE UNIVERSE
### A documentary about quantum computing

---

## S00 — COLD OPEN

In December 1900, a German physicist named Max Planck stood in front of a meeting of the German Physical Society and proposed that energy comes in lumps.

He did not believe it. He thought it was a trick. A mathematical convenience, invented to fix a curve that the physics of his day could not explain. A hot object glows red, then orange, then white, and nobody could say why. Planck found a formula that worked, but only if he assumed that energy is handed out in indivisible packets. He called them quanta. Then he spent years trying to make them go away.

They did not go away.

Within twenty-five years, that trick had become quantum mechanics: the most accurate theory ever written down. More accurate than anything else in science. Tested to one part in a hundred billion. And still, a century later, nobody can tell you what it actually means.

That is where this film begins. Not with computers. With a question.

Is quantum mechanics a description of reality, or is it just the best bookkeeping we have ever managed? Does the universe really behave this way, or does the maths only pretend that it does?

Because something strange happened while physicists argued about that question. We stopped asking what the theory means and started asking what it can do. And the answer turned out to be: almost anything, if you can build the machine.

A quantum computer is not a faster computer. It is a different kind of thing. It does not compute with numbers. It computes with the rules that govern matter itself.

This is the story of how we got there. The people, the arguments, the photographs, the failures. And the machine we are building now — a machine that borrows the universe, and gives it back an answer.

---

[CHAPTER CARD]
### I. THE RELUCTANT REVOLUTION
*1900 — 1935*

## S01 — ACT I

Planck's trick was simple, and outrageous. If energy comes in lumps, then a hot object can only emit light in certain sizes of lump. Small lumps when it is cool, bigger lumps as it heats up. The curve comes out right. Perfectly right. Embarrassingly right.

But a lump is a strange thing for nature to make. A wave can be any size at all. A ripple in a pond can be a millimetre or a mile. A lump has to be exactly one lump.

In 1905, a young patent clerk in Bern took the idea seriously. Albert Einstein argued that light itself is made of lumps. Photons. And that this explains the photoelectric effect: shine light on a metal, and electrons come off — but only if the light is the right colour, no matter how bright it is. Brighter red light does nothing. Dim blue light works immediately.

Einstein called these packets light quanta. He did not call them photons; that word came later. What matters is that he meant it literally. Not a trick. Not bookkeeping. Light, he said, is a thing that arrives in pieces.

He won the Nobel Prize for that, by the way. Not for relativity. For the lumps.

Then in 1913, a young Dane named Niels Bohr pointed the same logic at the atom. Electrons, he said, cannot orbit a nucleus at any distance they like. They are only allowed certain orbits. Certain energies. Jump between them, and the atom emits or absorbs a photon of exactly the right colour.

It worked. Hydrogen's spectrum — those thin bright lines that had been measured in laboratories and puzzled over for decades — fell out of the arithmetic. The atom had a staircase, not a ramp.

And then the staircase collapsed into something much stranger.

In 1924, Louis de Broglie asked the question nobody had thought to ask. If waves can behave like particles, why shouldn't particles behave like waves? An electron, he suggested, is a wave. A tiny, restless, standing wave.

Three years later, in 1927, physicists took a photograph that made the idea impossible to ignore. In Aberdeen, a young man named George Paget Thomson fired electrons at a thin metal foil. They came out as rings. Diffraction rings. The kind you get from waves. The kind you get from light.

Electrons were waves. And they were particles. At the same time. Depending on how you looked.

That photograph is one of the most important images in the history of science, and almost nobody has seen it.

By then, the theory had already been rewritten twice. In 1925, Werner Heisenberg, stranded on a windswept island in the North Sea with hay fever, invented a mathematics in which quantities do not commute — where A times B is not the same as B times A. He did not know what it meant. Neither did anyone else.

A year later, Erwin Schrödinger wrote down an equation that described the electron as a wave, spreading through space. It was beautiful, and it was wrong in the way that all useful things are wrong. It described the wave. It did not describe what the wave was.

Max Born supplied the answer that nobody wanted. The wave is not the electron. The wave is a probability. Square it, and you get the odds of finding the electron here rather than there.

Nature, at bottom, is a casino.

Einstein hated that. He wrote to Born in 1926: "Quantum mechanics is certainly imposing. But an inner voice tells me that it is not yet the real thing. The theory says a lot, but does not really bring us any closer to the secret of the 'old one.' I, at any rate, am convinced that He is not playing at dice."

He was wrong. Or he was right. We still don't know.

In 1927, the two sides met in Brussels. The fifth Solvay Conference. Twenty-nine physicists in one room, seventeen of whom would win Nobel Prizes. The photograph from that week is the most famous group portrait in science: Einstein in the front row, Bohr beside him, Marie Curie between them, Heisenberg and Pauli standing behind.

They argued about whether the universe is deterministic. Einstein kept proposing thought experiments designed to break quantum mechanics. Bohr kept answering them, sometimes overnight, sometimes at breakfast.

And in 1935, Einstein, Podolsky and Rosen published the sharpest version of the objection. Take two particles that interact, then separate them by a light-year. Measure one, and you instantly know something about the other. Not because you disturbed it — because the theory says the two were never really separate.

Einstein called it "spooky action at a distance." He meant it as an insult.

It was a measurement.

---

[CHAPTER CARD]
### II. INFORMATION IS PHYSICAL
*1961 — 1996*

## S02 — ACT II

For thirty years after Solvay, quantum mechanics was a tool. It worked. It predicted the spectra of atoms, the behaviour of semiconductors, the colour of the sky. Physicists used it every day and argued about its foundations at conferences, and the two activities barely touched.

Then in 1961, an IBM engineer named Rolf Landauer noticed something that should have been obvious, and wasn't.

Information is physical.

If you store a bit — a one or a zero — you need something to store it in. A magnet, a charge, a photon. And if you erase that bit, you have to dump the information somewhere. Landauer calculated the cost: at least kT ln 2 of energy, where k is Boltzmann's constant and T is temperature. A tiny number. But not zero.

Erasing information is not free, because information is not abstract. It is a physical state of a physical system. To destroy it, you have to pay.

That idea travelled quietly for a decade. In 1973, Charles Bennett at IBM took it further: if erasing is what costs energy, then a computation that never erases anything could, in principle, be free. Reversible computation. Logic gates that run backwards as easily as forwards.

Bennett was thinking about thermodynamics. He got something else.

Because a reversible gate is a gate that keeps all of its inputs. It doesn't throw anything away. And in 1980, a young physicist named Paul Benioff pointed out that a quantum system, evolving according to Schrödinger's equation, is also reversible. The equation runs backwards perfectly. So why not build a computer out of quantum systems?

Benioff's paper was almost ignored. It was too early, and it was too strange. But it was the first sketch of the idea.

The idea got its voice in 1981, at a conference in Boston, from Richard Feynman.

Feynman was not trying to invent a computer. He was trying to simulate physics. And he had noticed a problem. A classical computer simulating a quantum system has to track every possible state, and the number of possible states grows exponentially. Thirty particles, and you are already out of memory. Three hundred, and you need more bits than there are atoms in the observable universe.

Feynman's suggestion was almost cheeky. If a classical computer is too slow to simulate quantum mechanics, build a computer that is quantum mechanical. Let nature do the calculation.

"Nature isn't classical, dammit," he said, "and if you want to make a simulation of nature, you'd better make it quantum mechanical."

The room laughed. He wasn't joking.

In 1985, David Deutsch, a young physicist at Oxford, turned Feynman's suggestion into a theory. He described a machine that could simulate any physical process — a universal quantum computer — and showed that it could do things no classical computer could do efficiently. Not just simulate physics. Compute.

Deutsch's paper is where the field really begins. It is also where the trouble begins, because Deutsch was careful. He said the machine would work. He did not say how to build one.

Then in 1994, a mathematician at Bell Labs named Peter Shor found the first thing that would actually be worth building.

Shor was working on a problem that had been open for centuries: factoring. Given a large number, find the primes that multiply together to make it. Classical computers can do it, but slowly. Double the size of the number, and the time roughly doubles with it. For a 600-digit number, the best algorithms would take longer than the age of the universe.

Shor found a way to do it in polynomial time — if you had a quantum computer. Not a small improvement. An entirely different scaling law. A 600-digit number becomes a few weeks of work.

The reason it works is beautiful, and worth stating plainly. Factoring is really a question about periodicity: find the repeating pattern hidden in the powers of a number. And a quantum computer is very good at finding repeating patterns, because it can be in many states at once, and those states interfere.

Interference is the whole trick. Not parallel universes. Not magic. Waves adding up and cancelling out.

A quantum computer is an interference machine. It sets up a superposition in which every wrong answer cancels, and the right answer survives. Then you measure.

Two years later, Lov Grover found a second trick: searching an unsorted list. A classical computer has to check every item. A quantum computer can do it in about the square root of the number of steps. For a billion items, that is thirty thousand steps instead of a billion. Not exponential. Still enormous.

By 1996, the field had a theory, two algorithms, and no hardware. It had mathematicians, computer scientists, and a growing number of physicists who suspected the whole thing was impossible.

Because a quantum computer has a problem that no classical computer has. It is made of the same fragile stuff it is trying to compute with. And the moment it touches the outside world, it falls apart.

---

[CHAPTER CARD]
### III. THE MACHINE
*1995 — 2020*

## S03 — ACT III

The problem is called decoherence, and it is not a small engineering detail. It is the central fact of quantum computing.

A qubit is a quantum system with two states. Not a bit that is both zero and one — that is a cartoon. A qubit is a system described by two complex numbers, amplitudes, whose squares give the probability of measuring zero or one. Before measurement, it can be in a superposition. After measurement, it is not.

Everything in between is coherence. The amplitudes have to stay in a precise relationship, with a precise phase, for the computation to work. And almost everything destroys that relationship. A stray photon. A vibrating atom. A cosmic ray. Heat.

So the first thing you need is cold. Not refrigerator cold. Ten millikelvin. Colder than the cosmic microwave background, which is 2.7 kelvin. Colder than anything in the solar system.

That is what a dilution refrigerator is for. It is the machine you have seen in photographs without knowing what you were looking at: a gold-plated chandelier, hanging in a cylinder, surrounded by layers of shielding. At the bottom, a chip the size of a fingernail, sitting at a temperature where the thermal noise is slower than the computation.

The second thing you need is isolation. The chip is shielded from magnetic fields, from radio waves, from vibration. The room around it is a Faraday cage. The wiring that carries signals in is filtered, attenuated, and carefully routed, because a single stray microwave photon can ruin a calculation.

And the third thing you need is speed. A superconducting qubit holds its state for tens or hundreds of microseconds. A gate takes tens of nanoseconds. That is a ratio of thousands. You have time for a few thousand operations before the state decays. Not millions. Thousands.

This is why error correction is not optional.

The first real qubits were built in the late 1990s. In 1995, Juan Ignacio Cirac and Peter Zoller proposed a way to trap ions with electric fields and manipulate them with lasers. In 1999, a team at NEC in Japan, led by Yasunobu Nakamura, built a superconducting qubit — a tiny circuit with a Josephson junction, behaving like an artificial atom. Both approaches are still with us.

In 2000, David DiVincenzo wrote down the five criteria a quantum computer has to satisfy. Qubits that can be initialized. A universal set of gates. Long coherence times. A way to read out. And a way to scale.

That list is still the field's report card.

For the next fifteen years, the numbers improved slowly. One qubit became two, then five, then twenty. Fidelities climbed from ninety percent to ninety-nine, then ninety-nine point nine. Each decimal place was a thesis, a career, a decade.

And then, in 2019, Google put a machine called Sycamore in front of the world and claimed it had done something no classical computer could do.

Sycamore had 53 superconducting qubits. The task was random circuit sampling: run a random sequence of gates, measure, repeat. It is deliberately useless. It produces no answer anyone wants. It is a stress test — a way of asking whether the machine can hold a quantum state long enough to do something a classical computer cannot follow.

Google said Sycamore had done in 200 seconds what would take a classical supercomputer ten thousand years.

IBM immediately disagreed. Their analysis said the same calculation could be done on a classical machine in two and a half days. Not ten thousand years. Two and a half days.

Both numbers were defensible. That is the problem with the word "supremacy."

The claim was not that quantum computers are useful. It was that a quantum machine had crossed a line. And the line kept moving, because classical algorithms kept getting better, and classical hardware kept getting faster.

What survived the argument was something more interesting than the claim. Sycamore proved that a programmable quantum machine with more than fifty qubits could be built, calibrated, and run. It proved that the engineering was real.

The theory had been waiting thirty-five years for that.

---

[CHAPTER CARD]
### IV. THE ERROR
*2019 — 2024*

## S04 — ACT IV

Here is the uncomfortable arithmetic of quantum computing.

A physical qubit is bad. It fails. Not occasionally — constantly. Coherence decays. Gates are imperfect. Readout is noisy. The best qubits in the world, in 2024, had error rates around one in a thousand per gate. That sounds good. It is catastrophic.

A useful algorithm might need a billion gates. At one in a thousand, the computation is destroyed long before it finishes. Even at one in ten thousand, you lose.

The solution is not better qubits, though better qubits help. The solution is to stop using physical qubits and start using logical ones: a logical qubit made of many physical qubits, wired together so that they correct each other's errors.

This is quantum error correction, and it is the most important idea in the field.

The simplest version is the surface code. Imagine a grid of qubits. Some hold data. Some are measured constantly, checking the parity of their neighbours. When a measurement flips, you know something went wrong nearby. You don't know what, and you don't need to. You just need enough checks to localise the error and correct it.

The catch: you need a lot of physical qubits per logical qubit. Early estimates were thousands. Later ones, hundreds. And the whole scheme only works if the physical error rate is below a threshold — roughly one percent for the surface code.

Above the threshold, adding more qubits makes things worse. Below it, adding more qubits makes things better. That is the whole game. Get below threshold, and scale.

For twenty years, nobody could get below threshold. The qubits were too noisy, the grids too small, the measurements too slow.

In December 2024, Google published a result that changed that.

The machine was called Willow. It had 105 superconducting qubits, and it was designed to test one thing: whether increasing the size of the error-correcting grid actually reduced the error.

They built grids of distance three, five, and seven. A distance-seven surface code uses 49 physical qubits for one logical qubit. And they measured the logical error rate per cycle: 0.143 percent.

That number by itself is not impressive. What matters is the trend. Each time they increased the distance by two, the logical error rate fell by a factor of about 2.14. Not stayed the same. Fell.

For the first time, a quantum error-correcting code was performing better as it got bigger. Below threshold. The thing the theory promised, in hardware, on a chip.

The same paper included a second result, and this one made headlines. Willow ran a random circuit sampling benchmark in under five minutes. Google estimated that the same calculation would take a classical supercomputer ten septillion years — a one followed by twenty-five zeros.

That number is almost meaningless. It is a statement about one benchmark, on one day, against one classical algorithm. It is not a statement about useful computing. Google was careful about this in the paper. The press was not.

But the error-correction result is not meaningless. It is the first real evidence that the scaling law works. And scaling laws are how technology stops being a demonstration and starts being a tool.

There is a catch, and it is worth saying clearly. A logical qubit that fails once every thousand cycles is not a good qubit. Willow's logical qubit still fails far too often to run a long algorithm. The result is a proof of direction, not a proof of arrival.

To run Shor's algorithm against a 2,000-bit RSA key, you would need thousands of logical qubits, each made of hundreds of physical qubits, each operating for millions of cycles without failing. That is not one generation of hardware away. It might be three.

And yet, the direction is now established. Before Willow, below-threshold was a hope. After Willow, it is a measurement.

---

[CHAPTER CARD]
### V. THE RACE
*2025 — 2026*

## S05 — ACT V

So where are we, actually?

The honest answer is: further than the headlines suggest, and much further from the finish line than the headlines imply.

There are now five or six serious approaches, and none of them has won.

Superconducting circuits are the most mature. Google, IBM, and a cluster of startups use them. They are fast — gates in nanoseconds — and they are manufactured with the tools of the semiconductor industry. Their weakness is wiring. Every qubit needs control lines, and at a million qubits the wiring problem becomes a manufacturing problem of its own. IBM's answer is to move the control electronics into the fridge, stacked in layers above the chip.

Trapped ions are the most precise. Quantinuum's machines hold a handful of ions in an electromagnetic trap and manipulate them with lasers. Their gate fidelities are the best in the world — above 99.9 percent, in some cases above 99.99. Their weakness is speed. Gates take microseconds, not nanoseconds. And scaling means shuttling ions around a trap, which is delicate, brilliant, and slow.

Neutral atoms are the fastest-moving field. Instead of ions, you trap neutral atoms in arrays of laser light — optical tweezers — and you can arrange hundreds or thousands of them in arbitrary patterns. In 2023, a Harvard-led team used this approach to demonstrate 48 logical qubits, and the numbers have been climbing since. The weakness is that neutral-atom gates are slower and less precise than ion traps, and the lasers are power-hungry.

Photonic machines use light. They are attractive because photons don't decohere easily and they can travel down optical fibre. PsiQuantum is trying to build a fault-tolerant machine with silicon photonics, and has said it aims for a utility-scale system before the end of the decade. The weakness is that photons don't interact with each other easily, which makes two-qubit gates hard, and loss is brutal.

And then there is Microsoft, which is trying something entirely different.

In February 2025, Microsoft announced a chip called Majorana 1. It was not a general-purpose quantum processor. It was a demonstration of a new kind of qubit, based on a particle called a Majorana fermion — a particle that is its own antiparticle, predicted in 1937, never definitively observed.

Microsoft's claim was extraordinary. Topological qubits are protected by the topology of the material itself, not by careful control. They should be far more stable than any other kind. If they work, they could skip the error-correction problem almost entirely.

The announcement was met with excitement and deep scepticism, in roughly equal measure. The company published a Nature paper describing the physics, but the paper did not demonstrate a working topological qubit. It demonstrated evidence for the material platform. Independent physicists pointed out that the central signature — the presence of Majorana modes — has been claimed before and retracted. Microsoft itself had a 2018 paper retracted after the data could not be reproduced.

Is it real? The honest answer is: not yet proven. The company says it will have a scalable machine by the end of the decade. The physics community is watching, and waiting, and not convinced.

That is not cynicism. It is how the field works. Quantum computing has a long history of beautiful claims that did not survive contact with a lab.

The same month, Amazon announced a different approach: cat qubits. A cat qubit is a superconducting circuit designed so that one kind of error — bit flips — is exponentially suppressed. Amazon claimed a prototype with up to ninety percent reduction in that error channel. It is a real result, on a small device, and it addresses one half of the problem. The other half, phase errors, remains.

So the race is not a single race. It is a set of parallel bets on physics, and nobody knows which one pays.

What is not in doubt is the consequence.

In August 2024, NIST finalised the first post-quantum encryption standards: three algorithms designed to resist an attack by a quantum computer. ML-KEM, ML-DSA, SLH-DSA. They are already being deployed in browsers, phones, and secure messaging.

The reason is not that quantum computers can break encryption today. They cannot. The reason is "harvest now, decrypt later." An adversary can record encrypted traffic today and wait. If a large quantum computer arrives in fifteen years, everything recorded now becomes readable.

That is a strange kind of threat, because it is the first cryptographic threat that is entirely about the future. It assumes the machine will exist. It prepares for the possibility that it won't.

And that, in a way, is the whole story of quantum computing. We are building a technology on a bet about physics that we cannot yet fully verify.

---

[CHAPTER CARD]
### VI. THE LEDGER

## S06 — CODA

So let's be honest about the ledger.

What a quantum computer will probably do, if it works:

It will simulate molecules. Not approximately, the way classical computers do, but natively — because a molecule is a quantum system, and the machine speaks its language. That could mean better catalysts, better batteries, better fertiliser. Nitrogen fixation alone consumes about one to two percent of the world's energy, and a quantum computer might find a catalyst that does it at room temperature.

It will break some encryption, and it will help build better encryption. Both. That is not a contradiction; it is what happens when you change the rules of computation.

It will probably not make your phone faster. It will not run video games. It will not replace your laptop. For almost everything, a classical computer is better, and will stay better. A quantum computer is a specialised instrument, like a particle accelerator or a telescope. You don't put one in your pocket. You build one, and you point it at a problem.

What it might do, and this is the part that matters:

It might fail. Not because the physics is wrong, but because the engineering is too hard. The wiring, the cooling, the error rates, the cost. There is a real chance that in fifty years, quantum computing is remembered the way we remember fusion: always thirty years away.

And what it will definitely do, whether or not it ever factors a single number:

It will force us to answer the question Planck avoided.

Because a quantum computer is not a metaphor. It is a physical object that behaves according to quantum mechanics, and produces results that a classical object cannot. If it works — if you can actually run a computation that no classical machine can follow — then the theory is not just useful. It is, in some sense, true. The superposition was real. The interference was real. The universe really does keep all those possibilities alive until you look.

That is not a philosophical claim. It is an engineering claim, and it is being tested right now, in refrigerators the size of a person, at ten millikelvin, one cycle at a time.

Planck spent his life trying to prove that the quanta were a mistake. He never succeeded. He died in 1947, a few years before the transistor, decades before the first quantum computer. He never saw what his trick would become.

But he knew. In a letter near the end of his life, he wrote that the new quantum theory would one day be understood as a bridge — a temporary structure between the physics he had inherited and a physics nobody had yet imagined.

We are still crossing that bridge.

The machine at the end of it is not a faster calculator. It is the first machine we have ever built that does not approximate nature. It borrows nature, and gives it back an answer.

And if the answer is yes — if the universe really is made of quanta, and superposition, and probabilities that collapse only when someone looks — then the most beautiful idea in physics is not one we proved.

It is one we are still learning to operate.
