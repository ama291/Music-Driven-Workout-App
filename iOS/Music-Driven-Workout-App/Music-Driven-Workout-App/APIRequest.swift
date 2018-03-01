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
    
    func parseJsonStrToDictArrayWithKey(str: String, key: String) -> [[String:Any]] {
        let dict = parseJsonResponeSingleDict(str: str)
        let arrayStr = dict![key]
        print(arrayStr, "arrayStr")
        let arrayDict = arrayStr as! [[String:Any]]
        print(arrayDict[0]["bpm"]!, "0 bpm")
        return arrayDict
    }
    
    func parseJsonStrToDictArray(str: String) -> [[String:Any]]? {
        let data = str.data(using: .utf8)
        var reply: [[String:Any]]
        do {
            reply = try JSONSerialization.jsonObject(with: data!, options: []) as! [[String:Any]]
            let myReplyDict = reply
            return myReplyDict
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
    
    func parseJsonResponeSingleDict(str: String) -> [String:Any]? {
        let data = str.data(using: .utf8)
        var reply: [String:Any]
        do {
            reply = try JSONSerialization.jsonObject(with: data!, options: []) as! [String:Any]
            let myReplyDict = reply
            return myReplyDict
        } catch let error {
            print(error)
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
