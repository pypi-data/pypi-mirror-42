# Huskarl
Huskarl is a Deep Reinforcement Learning Framework     modern framework for deep reinforcement learning focused on research and prototyping.
It is built on TensorFlow 2.0 and uses the `tf.keras` API when possible for conciseness and readability.

Huskarl makes it easy to parallelize computation of environment dynamics across multiple CPUs. This is useful for speeding up on-policy learning algorithms that require multiple sources of experience for variance reduction such as A2C or PPO. It is specially useful for computationally intensive environments such as physics-based ones.

You can pause, and restart simulations with ease. Huskarl also autosaves your model's parameters and training graphs (and memory?) so if something happens, like running out of RAM you can easily pick up training from where you left off.


create_env can create slightly different environments, which is useful for example in robotics where you want your model to adapt to different physical properties - TODO: reword, find paper from Pieter Abeel


Ray(linkme!) is used for parallelization, allowing computation to scale massively over multiple CPUs and GPUs. (TPUs as well?).
Unlike Ray's RLlib, Huskarl allows for complex environment-agent relationships e.g. multiple agents per environment and multiple insertions(define nomenclature) per agent.



# TODO project called Valhalla - environments for Huskarl

# TODO create demos that load pre-trained agents in complex environments like Atari games


## Algorithms

TODO: Link papers below:

* [x] Deep Q-Learning Network (DQN)
	* [x] Multi-step Q-Learning
	* [x] Double Q-Learning
	* [x] Dueling Q-Network
* [ ] Deep SARSA
* [ ] Curiosity
* [ ] Proximal Policy Optimization (PPO)
* [ ] Synchronous Advantage Actor-Critic (A2C)

## Environment

Huskarl environments are very flexible and general, allowing for multiple agents per environment, and multiple insertion points for each agent e.g. for self-play.

[DIAGRAM OF RELATIONSHIPS]


Huskarl works seamlessly with OpenAI Gym environments, and also Unity3D environments.

## Installation
todo

## Citing

TODO

## About

"hùskarl" in Old Norse means a warrior who works in his/her lord's service.
The name also ends in -rl alluding to Reinforcement Learning.