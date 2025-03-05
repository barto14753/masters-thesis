# `Analysis of attacks on language models`

- _Author_: `Bartosz Włodarski`
- _Supervisor_:
- _University_: `Cracow University of Technology`
- _Faculty_: `Faculty of Computer Science and Telecommunications`
- _Field of study_: `Computer Science`
- _Specialization_: `Cybersecurity`
- _Degree_: `Master of Engineering`
- _Language_: `English`
- _Year_: `2024-2025`

## Overview:

1. Introduction to Language Models

   - The Transformer architecture and its significance
   - Key models (GPT, BERT, T5)
   - Training and fine-tuning processes
   - Tokenization and its impact on security

2. OWASP GenAI Top 10

   - Detailed analysis of each threat
   - Practical examples of vulnerabilities
   - Methods for detecting vulnerabilities
   - Recommended mitigations

3. Types of Attacks on Language Models

   - Prompt injection
   - Prompt leaking
   - Dictionary attacks
   - Jailbreaking
   - Attacks on tokenization
   - Data poisoning
   - Model extraction
   - Membership inference attacks
   - Adversarial examples

4. Security Measures

   - Input sanitization
   - Output validation
   - Prompt hardening
   - Rate limiting
   - Behavioral monitoring
   - Systematic security evaluation

5. Tools for Security Analysis

   - LLM-Guard
   - PromptMap
   - Langchain Security
   - Custom security wrappers
   - Penetration testing tools

6. Case Studies

   - Known attacks and incidents
   - Root cause analysis
   - Lessons learned
   - Applied remediations

7. Legal and Ethical Aspects

   - Responsibility for AI actions
   - GDPR and data privacy
   - Ethical AI guidelines
   - Industry standards

8. Best Practices for Securing Models

   - Secure AI system architectures
   - Development processes
   - Security testing
   - Production monitoring
   - Incident response

9. Future of AI Security

   - Emerging threats
   - New defense methods
   - Trends in security development
   - Anticipated regulations

10. Practical Workshops

    - Implementation of basic security measures
    - Vulnerability testing
    - Building secure-by-design systems
    - Analysis of test cases

11. Security Metrics and Measurements

    - Security KPIs for AI systems
    - Methods for evaluating security
    - Benchmarking security tests
    - Continuous security monitoring

## OWASP

1. LLM01: Prompt Injection
   Manipulating LLMs via crafted inputs can lead to unauthorized access, data breaches, and compromised decision-making.

2. LLM02: Insecure Output Handling
   Neglecting to validate LLM outputs may lead to downstream security exploits, including code execution that compromises systems and exposes data.

3. LLM03: Training Data Poisoning
   Tampered training data can impair LLM models leading to responses that may compromise security, accuracy, or ethical behavior.

4. LLM04: Model Denial of Service
   Overloading LLMs with resource-heavy operations can cause service disruptions and increased costs.

5. LLM05: Supply Chain Vulnerabilities
   Depending upon compromised components, services or datasets undermine system integrity, causing data breaches and system failures.

6. LLM06: Sensitive Information Disclosure
   Failure to protect against disclosure of sensitive information in LLM outputs can result in legal consequences or a loss of competitive advantage.

7. LLM07: Insecure Plugin Design
   LLM plugins processing untrusted inputs and having insufficient access control risk severe exploits like remote code execution.

8. LLM08: Excessive Agency
   Granting LLMs unchecked autonomy to take action can lead to unintended consequences, jeopardizing reliability, privacy, and trust.

9. LLM09: Overreliance
   Failing to critically assess LLM outputs can lead to compromised decision making, security vulnerabilities, and legal liabilities.

10. LLM10: Model Theft
    Unauthorized access to proprietary large language models risks theft, competitive advantage, and dissemination of sensitive information.

## Links

- https://www.youtube.com/watch?v=jrHRe9lSqqA&ab_channel=IBMTechnology
- https://genai.owasp.org/
- https://learnprompting.org/docs/prompt_hacking/introduction
- https://github.com/Seezo-io/llm-security-101
- https://github.com/protectai/llm-guard
- https://github.com/utkusen/promptmap
- https://www.algolia.com/blog/ai/prompt-injection/
- https://www.youtube.com/watch?v=S5MKPtRpVpY&ab_channel=NDCConferences
