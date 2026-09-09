from abc import ABC,abstractmethod
class VerificationProvider(ABC):
 @abstractmethod
 def verify(self,data): raise NotImplementedError
class ManualVerificationProvider(VerificationProvider):
 def verify(self,data): return {"status":"MANUAL_REVIEW","source":"MANUAL_VERIFICATION_REQUIRED","confidence":None,"details":{},"errors":["No approved official API credentials are configured."],"requires_manual_review":True}
