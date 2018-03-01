import UIKit

class APIRequest: NSObject {
    
    func parseJsonInitial(data: Data) -> String? {
        var res: Dictionary<String, String>
        do {
            res = try JSONSerialization.jsonObject(with: data, options: []) as! Dictionary<String, String>
            let myDict = res
            if let result = myDict["Result"] {
                return result
            }
            
        } catch let error {
            print(error)
        }
        return nil
        
    }
    
    func parseJsonGeneric(data: String, key: String) -> String? {
        var res: Dictionary<String, String>
        let resultData = data.data(using: String.Encoding.utf8)
        do {
            res = try JSONSerialization.jsonObject(with: resultData!, options: []) as! Dictionary<String, String>
            let myDict = res
            if let result = myDict[key] {
                return result
            }
            
        } catch let error {
            print(error)
        }
        return nil
        
    }
    
    
    func parseJsonRespone(data: Data) -> [Dictionary<String, Any>]? {
        if let result = parseJsonInitial(data: data) {
            var reply: [Dictionary<String, Any>]
            
            if let resultData = result.data(using: String.Encoding.utf8) {
                do {
                    reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [Dictionary<String, Any>]
                    let myReplyDict = reply
                    return myReplyDict
                } catch let error {
                    print(error)
                }
            }
        }
        return nil
    }
    
    func parseJsonResponseFromString(str: String) -> [Dictionary<String, Any>]? {
        let data = str.data(using: .utf8)
        if let result = parseJsonInitial(data: data!) {
            var reply: [Dictionary<String, Any>]
            
            if let resultData = result.data(using: String.Encoding.utf8) {
                do {
                    reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [Dictionary<String, Any>]
                    let myReplyDict = reply
                    return myReplyDict
                } catch let error {
                    print(error)
                }
            }
        }
        return nil
    }
    
    func parseJsonResponeSingleDict(data: Data) -> String? {
        if let result = parseJsonInitial(data: data) {
            var reply: [String:Any]
            
            if let resultData = result.data(using: String.Encoding.utf8) {
                do {
                    reply = try JSONSerialization.jsonObject(with: resultData, options: []) as! [String:Any]
                    let myReplyDict = reply
                    return myReplyDict["Result"] as? String
                } catch let error {
                    print(error)
                }
            }
        }
        return nil
    }
    
    func submitPostLocal(route: String, qstring: String, completion: @escaping (Data?, URLResponse?,Error?) -> Void) -> URLSessionDataTask {
        var urlComponents = URLComponents()
        urlComponents.scheme = "http"
        urlComponents.host = "127.0.0.1"
        urlComponents.port = 5000
        urlComponents.path = route
        urlComponents.query = qstring
        guard let url = urlComponents.url else {
            fatalError("Could not create URL")
        }
        print(url)
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let postString = qstring
        request.httpBody = postString.data(using: String.Encoding.utf8)
        print("jsonData: ", String(data: request.httpBody!, encoding: .utf8) ?? "no body data")
        
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        let task = session.dataTask(with: request) {(data, response, responseError) in
            if let data = data {
                completion(data, response, responseError)
            }
        }
        return task
    }
    
}
